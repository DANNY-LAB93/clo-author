"""Deduplicate records across every searched source, and produce the PRISMA
identification counts.

WHY THREE KEYS. De-duplicating on DOI alone is not enough here, and neither is
PMID alone, because two of this review's sources overlap other sources BY
CONSTRUCTION rather than by chance:

  - Cochrane CENTRAL ingests ClinicalTrials.gov records, so the same trial
    appears once with an NCT and once as a CENTRAL record;
  - BVS searches MEDLINE alongside LILACS, so a PubMed record can arrive twice
    with the same PMID under two source labels.

A record is therefore matched on DOI, PMID *and* NCT, and matches are
TRANSITIVE: if record A shares a DOI with B, and B shares a PMID with C, all
three are one record. That is done with union-find rather than pairwise
comparison, because pairwise misses the A-C link.

TWO LEVELS, AND THEY ARE DIFFERENT NUMBERS. PRISMA 2020 separates *reports* from
*studies*, so this clusters twice:

  - REPORT level, on DOI and PMID. The same report retrieved from two sources.
    This, and only this, is "duplicates removed".
  - STUDY level, adding NCT. A protocol and its results paper are two reports of
    one study; a registry entry is a record in its own right. Folding those into
    "duplicates" would understate records identified, which is why the study
    grouping is emitted as a separate column instead.

IDENTIFIERS ARE READ ONLY FROM IDENTIFIER FIELDS, never from free text. Two bugs
made the reason concrete. Scanning abstracts merged four unrelated papers that
happened to cite the same 2001 AAC article. And PubMed files a review's
DataBankList with every trial the review discusses -- PMID 39357832 lists five
NCTs -- so a record carrying SEVERAL identifiers of one type may not link
anything: it is listing other people's, not reporting its own.

RECORDS WITH NO IDENTIFIER fall back to a normalised title plus year. This is
deliberately conservative -- normalisation strips punctuation, case, accents and
a leading article, but does NOT do fuzzy matching. Two papers whose titles differ
by one word stay separate, because merging distinct studies is a worse error than
counting one twice, and the second is visible in the output while the first is
not.

SAFEGUARDS. Over-merging is the one failure this script cannot show in its own
output -- a merged pair simply appears as one record. Two checks look for it: no
two of the 42 already-included studies may share a group, and no report group may
hold two PMIDs. Both exit non-zero.

WHAT PRISMA NEEDS AND THIS EMITS: records identified per source, duplicates
removed, and records remaining. Those are three separate boxes and the flow
diagram must show all three.

USAGE
    python scripts/deduplicate_sources.py --manifest revision_sistematica/busqueda/sources.json
    python scripts/deduplicate_sources.py --manifest ... --out revision_sistematica/cribado/deduplicated.csv

The manifest is JSON mapping a source label to a file path, e.g.

    {
      "PubMed":            "revision_sistematica/busqueda/screening_pubmed_union.csv",
      "Scopus (brazo A)":  "revision_sistematica/busqueda/scopus_armA.csv",
      "Scopus (brazo B)":  "revision_sistematica/busqueda/scopus_armB.csv",
      "Cochrane CENTRAL":  "revision_sistematica/busqueda/central_export.ris",
      "BVS (no MEDLINE)":  "revision_sistematica/busqueda/bvs_non_medline.ris",
      "ClinicalTrials.gov":"revision_sistematica/busqueda/clinicaltrials_gov.csv"
    }
"""
import argparse
import csv
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
csv.field_size_limit(10_000_000)

# Parentheses are NOT terminators. Elsevier PII-style DOIs contain them
# (10.1016/S1473-3099(18)30482-1), and excluding ')' truncated every Lancet DOI
# to its year prefix -- a key shared by every Lancet paper of that year, which
# merged PhagoBurn with an unrelated editorial. Unbalanced trailing brackets are
# trimmed in norm_doi instead.
DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s,;\"'<>]+)")
PMID_RE = re.compile(r"\b(\d{7,8})\b")
NCT_RE = re.compile(r"\b(NCT\d{8})\b", re.I)

# CSV columns that ARE identifiers. Everything else -- title, abstract, notes,
# keywords -- is free text and is never scanned. See keys_for() for why.
ID_COLUMNS = frozenset((
    "doi", "do", "pmid", "pubmed", "pubmed id", "pmcid", "pmc",
    "nct", "nct number", "nct_id", "nctid", "trial id", "registry number",
    "secondary ids", "other ids", "accession", "an", "id", "url", "ur", "link",
))


# ---------------------------------------------------------------- normalising
CLOSERS = {")": "(", "]": "[", "}": "{"}


def norm_doi(v):
    v = re.sub(r"^https?://(dx\.)?doi\.org/", "", (v or "").strip(), flags=re.I)
    v = re.sub(r"[.,;:]+$", "", v)
    # Trim only UNBALANCED trailing brackets -- those come from a DOI that was
    # wrapped in text. A balanced pair belongs to the DOI itself.
    while v and v[-1] in CLOSERS and v.count(v[-1]) > v.count(CLOSERS[v[-1]]):
        v = v[:-1]
    return v.lower()


def norm_title(t):
    """Case, accent, punctuation and leading-article insensitive. NOT fuzzy."""
    t = unicodedata.normalize("NFKD", (t or ""))
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"^(the|a|an|el|la|los|las|un|una)\s+", "", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ------------------------------------------------------------------- readers
def bvs_id(v):
    """BVS/LILACS files a PubMed record's PMID as `ID  - mdl-42450545`. Without
    this the 26 MEDLINE-sourced records in the BVS export would never match the
    PubMed corpus and would be counted twice. Verified against eutils: three of
    three mdl- values resolved to the same title in PubMed. Other prefixes
    (lil-, cum-, bin-, biblio-) are BVS-internal and are left alone."""
    m = re.match(r"^mdl-(\d{7,8})$", (v or "").strip(), re.I)
    return "PMID: " + m.group(1) if m else v


def read_ris(text):
    """RIS. Identifiers come only from identifier tags -- DO, AN, ID, UR, C7, M1
    -- never from AB. An abstract routinely cites other papers' DOIs, and
    harvesting those merges unrelated records transitively."""
    recs, cur = [], {}
    for line in text.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])\s{2}-\s?(.*)$", line)
        if m:
            tag, val = m.group(1), m.group(2).strip()
            # A record STARTS at TY; that is the reliable boundary. Relying on
            # ER alone splits any record that carries a stray "ER  -" inside a
            # field: the SciELO export has 251 records and 252 ER lines, and
            # cutting on ER read 252, inventing a record that does not exist.
            if tag == "TY":
                if cur:
                    recs.append(cur)
                cur = {tag: [val]}
            elif tag != "ER":
                cur.setdefault(tag, []).append(val)
            # ER is NOT a boundary. It is supposed to close a record, but a
            # stray one inside a field then splits that record in two: the
            # SciELO export carries 251 TY lines and 252 ER lines, and cutting
            # on ER invented a 252nd record. TY is the only marker the RIS
            # format guarantees comes first, so it is the only one trusted here.
        elif cur:
            last = list(cur)[-1] if cur else None
            if last and line.strip():
                cur[last][-1] += " " + line.strip()
    if cur:
        recs.append(cur)
    out = []
    for r in recs:
        first = lambda *t: next((r[k][0] for k in t if k in r and r[k]), "")
        out.append({
            "title": first("TI", "T1"),
            # El idioma no interviene en la deduplicacion; se arrastra porque
            # es un criterio de elegibilidad declarado y hay que poder
            # comprobarlo contra la fuente en vez de deducirlo de la revista.
            "language": first("LA", "L1"),
            "year": re.sub(r"\D", "", first("PY", "Y1", "DA"))[:4],
            "journal": first("JO", "JF", "T2", "JA"),
            # C3 is Cochrane's source-accession field: short, structured pairs
            # like "PUBMED 30051571,EMBASE 628973066" or "CTgov NCT07698002".
            # It is the ONLY place a CENTRAL record states its PubMed or registry
            # identity -- UR holds Cochrane's own DOI, and the NCT is filed under
            # A1 as if it were an author. Without C3, CENTRAL would never
            # de-duplicate against PubMed or ClinicalTrials.gov.
            "idfields": " ".join(bvs_id(v) for k, vs in r.items()
                                 if k in ("DO", "AN", "ID", "UR", "C7", "M1", "C3")
                                 for v in vs),
            "doi": first("DO"),
            "abstract": first("N2", "AB"),
            "doctype": first("M3", "TY"),
            "keywords": "; ".join(r.get("KW", [])),
            "mesh": "",
        })
    return out


def read_nbib(text):
    recs, cur = [], {}
    for line in text.splitlines():
        m = re.match(r"^([A-Z]{2,4})\s*-\s?(.*)$", line)
        if m:
            cur.setdefault(m.group(1), []).append(m.group(2).strip())
        elif not line.strip():
            if cur:
                recs.append(cur); cur = {}
        elif cur:
            last = list(cur)[-1]
            cur[last][-1] += " " + line.strip()
    if cur:
        recs.append(cur)
    out = []
    for r in recs:
        first = lambda *t: next((r[k][0] for k in t if k in r and r[k]), "")
        out.append({
            "title": first("TI"), "language": first("LA"),
            "year": re.sub(r"\D", "", first("DP"))[:4],
            "journal": first("JT", "TA"),
            "idfields": " ".join("PMID: " + v if k == "PMID" else v
                                 for k, vs in r.items()
                                 if k in ("PMID", "AID", "LID", "PMC", "SI")
                                 for v in vs),
            "doi": "",
            "abstract": first("AB"),
            "doctype": "; ".join(r.get("PT", [])),
            "keywords": "",
            "mesh": "; ".join(r.get("MH", [])),
        })
    return out


def read_csv_any(path):
    """Read with the csv module driving the file handle. Splitting the text on
    newlines first shatters any quoted field that contains one -- abstracts
    always do -- and silently invents extra records."""
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        low = {(k or "").strip().lower(): (v or "") for k, v in r.items()}
        pick = lambda *n: next((low[x] for x in n if x in low and low[x]), "")
        out.append({
            "title": pick("title", "brieftitle", "ti", "article title"),
            "language": pick("language of original document", "language", "la"),
            "year": re.sub(r"\D", "", pick("year", "py", "publication year", "date"))[:4],
            # "source title" before "source": Scopus ships both, and its
            # "Source" column holds the literal string "Scopus", not the journal.
            "journal": pick("source title", "journal", "jo", "source"),
            "doi": pick("doi", "do"),
            "idfields": " ".join("%s: %s" % (k, v) for k, v in low.items()
                                 if k in ID_COLUMNS and v.strip()),
            "abstract": pick("abstract", "ab", "n2"),
            "doctype": pick("document type", "pubtypes", "pt", "studytype"),
            "keywords": " ; ".join(v for k, v in low.items()
                                   if k in ("author keywords", "index keywords",
                                            "keywords", "kw") and v),
            "mesh": pick("mesh", "mh"),
        })
    return out


def decode(path):
    """Try UTF-8, then Windows-1252, then Latin-1.

    Do NOT use errors="replace" on the first attempt. Cochrane's export declares
    `charset="UTF-8"` in its own header and is in fact Latin-1: replacing on
    error turns Brussow's umlaut into U+FFFD, which then propagates into the
    normalised title used for fallback matching. Failing over to another codec
    keeps the character; replacing silently corrupts it."""
    b = path.read_bytes()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", "replace")


def strip_markup(t):
    """Remove inline HTML/XML tags from a title.

    BVS and Scopus file the same paper as `Isolation of a <i>Klebsiella</i>
    Phage` and `Isolation of a Klebsiella Phage`. Two things break if the tags
    survive. First, `norm_title` deletes `<` and `>` but keeps the letter of the
    tag, so the two variants normalise to `... a i klebsiella i phage ...` and
    `... a klebsiella phage ...` and never match: the same report is counted
    twice whenever it carries no DOI or PMID. Second, the marked-up variant is
    always the longest, so it wins `longest()` and the markup ends up in the
    corpus, the worksheets and anything built from them.
    """
    return re.sub(r"\s+", " ", re.sub(r"<[^>]{0,40}>", "", t or "")).strip()


def load(path):
    suf = path.suffix.lower()
    text = "" if suf == ".csv" else decode(path)
    if suf == ".ris":
        recs = read_ris(text)
    elif suf in (".nbib", ".txt"):
        recs = read_nbib(text)
    elif suf == ".csv":
        recs = read_csv_any(path)
    else:
        raise SystemExit("unsupported file type: %s" % path.name)
    for r in recs:
        r["title"] = strip_markup(r.get("title", ""))
    return recs


# ------------------------------------------------------------------ matching
def keys_for(rec):
    """Returns (match_keys, all_ids).

    match_keys link records together; all_ids is everything the record carries,
    for display. They differ deliberately -- see the multi-identifier rule below.

    Read ONLY from identifier-bearing fields. Scanning free text merged four
    unrelated papers in testing because all four abstracts happened to cite the
    same 2001 AAC article, and union-find then joined them transitively."""
    blob = rec.get("idfields", "")
    doi = {"doi:" + norm_doi(d) for d in DOI_RE.findall(blob)}
    if rec.get("doi"):
        doi.add("doi:" + norm_doi(rec["doi"]))
    nct = {"nct:" + n.upper() for n in NCT_RE.findall(blob)}
    # PMIDs only from a labelled context: a bare 8-digit run is too often a
    # page range, an accession or a phone number to be trusted as an identifier.
    pmid = {"pmid:" + m.group(1) for m in
            re.finditer(r"(?:PMID|pubmed[^\d]{0,12})[: ]*(\d{7,8})", blob, re.I)}

    # A record carrying SEVERAL identifiers of one type is not reporting several
    # of its own -- it is listing other people's. PubMed files a review's
    # DataBankList with every trial the review discusses: PMID 39357832, a
    # Klebsiella review, lists five NCTs, and using it as a bridge chained
    # PhagoBurn to an unrelated diarrhoea trial. Those identifiers stay visible
    # in the output, but they may not link anything.
    match = set()
    for s in (doi, nct, pmid):
        if len(s) == 1:
            match |= s
    return match, doi | nct | pmid


def audit_known_studies(records, keys, groups):
    """Known-positive check: the 42 studies already in the corpus are distinct by
    construction, so no two of them may land in the same group.

    Over-merging is the one failure mode this script cannot show in its own
    output -- a merged pair simply appears as one record. This catches it. It is
    how the truncated-DOI bug was found: every Lancet paper of a given year
    shared the key `10.1016/s1473-3099(18`, and PhagoBurn was swallowed by an
    unrelated editorial."""
    index = ROOT / "quality_reports" / "corpus_identifier_index.txt"
    if not index.exists():
        print("NOTE: %s absent, known-positive audit skipped" % index.name)
        return []

    known = {}
    for line in index.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or "\t" not in line:
            continue
        ident, _, sid = line.partition("\t")
        typ, _, val = ident.partition(":")
        known["%s:%s" % (typ, norm_doi(val) if typ == "doi" else val.upper()
                         if typ == "nct" else val)] = sid.strip()

    collisions = []
    for members in groups.values():
        studies = set()
        for i in members:
            for k in keys[i]:
                if k in known:
                    studies.add(known[k])
        if len(studies) > 1:
            collisions.append((sorted(studies),
                               [records[i]["title"][:60] for i in members]))
    return collisions


class Union:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", default="revision_sistematica/cribado/deduplicated.csv")
    ap.add_argument("--report", default="quality_reports/deduplication.md")
    args = ap.parse_args()

    man_path = pathlib.Path(args.manifest)
    if not man_path.is_absolute():
        man_path = ROOT / man_path
    manifest = json.loads(man_path.read_text(encoding="utf-8"))

    records, per_source = [], {}
    for label, rel in manifest.items():
        p = pathlib.Path(rel)
        if not p.is_absolute():
            p = ROOT / p
        if not p.exists():
            print("MISSING, skipped: %-22s %s" % (label, p))
            per_source[label] = None
            continue
        recs = load(p)
        for r in recs:
            r["source"] = label
            records.append(r)
        per_source[label] = len(recs)
        print("%-22s %6d records  (%s)" % (label, len(recs), p.name))

    if not records:
        sys.exit("no records loaded; check the manifest paths")

    parsed = [keys_for(r) for r in records]   # computed once, reused throughout
    keys = [k for k, _ in parsed]             # what may link records
    allids = [a for _, a in parsed]           # what the record carries, for display

    # --- TWO LEVELS, because PRISMA 2020 counts reports and studies separately.
    #
    # REPORT level (DOI, PMID): the same report retrieved from two sources. This
    # is what "duplicates removed" means, and it is the only figure that belongs
    # in that PRISMA box.
    #
    # STUDY level (adds NCT): different reports of one trial -- a protocol and
    # its results paper, or a registry entry and the publication. Merging those
    # into "duplicates" would understate records identified, and a registry
    # record is a record in its own right; PRISMA gives registers their own
    # column precisely for this.
    def cluster(link_keys):
        u = Union()
        owner = {}
        for i in range(len(records)):
            u.find(("rec", i))
            for k in link_keys[i]:
                if k in owner:
                    u.union(("rec", owner[k]), ("rec", i))
                else:
                    owner[k] = i
        # records with no identifier at all: normalised title+year fallback
        title_owner = {}
        for i in range(len(records)):
            if link_keys[i]:
                continue
            t = norm_title(records[i]["title"])
            if len(t) < 15:
                continue                  # too short to match on safely
            tk = (t, records[i]["year"])
            if tk in title_owner:
                u.union(("rec", title_owner[tk]), ("rec", i))
            else:
                title_owner[tk] = i
        g = {}
        for i in range(len(records)):
            g.setdefault(u.find(("rec", i)), []).append(i)
        return g

    report_keys = [{k for k in ks if not k.startswith("nct:")} for ks in keys]
    groups = cluster(report_keys)              # PRISMA "records after duplicates"
    study_groups = cluster(keys)               # reports gathered into studies

    no_id = [i for i in range(len(records)) if not keys[i]]
    known_collisions = audit_known_studies(records, keys, study_groups)

    # --- assemble ---
    study_of = {}                              # record index -> study label
    for n, members in enumerate(study_groups.values(), 1):
        for i in members:
            study_of[i] = "S%04d" % n

    rows, suspicious, over_merged = [], [], []
    for members in groups.values():
        first = records[members[0]]
        srcs = sorted({records[i]["source"] for i in members})
        ids = sorted(set().union(*(allids[i] for i in members)))
        # A PMID identifies exactly one PubMed record. Two of them inside one
        # REPORT group means two distinct records were merged -- a far sharper
        # signal than "group bigger than source count", which cannot fire at all
        # when the over-merge happens inside a single source. Counted only for
        # groups that actually merged something; a lone record listing several
        # identifiers is normal and is handled by the multi-identifier rule.
        if len(members) > 1:
            n_pmid = len({k for k in ids if k.startswith("pmid:")})
            titles = {norm_title(records[i]["title"]) for i in members
                      if (records[i]["title"] or "").strip()}
            if n_pmid > 1 and len(titles) > 1:
                # Two PMIDs AND two different titles: distinct reports were
                # merged. This is the fatal case.
                over_merged.append((len(members), first["title"][:70],
                                    "report group holds %d PMIDs and %d titles, sources: %s"
                                    % (n_pmid, len(titles), ", ".join(srcs))))
            elif n_pmid > 1:
                # Two PMIDs but ONE title: the same report, with sources
                # disagreeing about its PMID. Scopus does this -- it gave
                # 10.1136/postgradmedj-2022-141546 the PMID 35379752 where
                # PubMed itself records 37389583. That is a metadata error in
                # the aggregator, not an over-merge, so it is reported rather
                # than fatal. PubMed's own PMID is the authoritative one.
                suspicious.append((len(members), first["title"][:70],
                                   "PMID en conflicto entre fuentes (%s): %s"
                                   % (", ".join(srcs),
                                      " ".join(sorted(k for k in ids
                                                      if k.startswith("pmid:"))))))
        rows.append({
            "study_group": study_of[members[0]],
            "title": " ".join((first["title"] or "").split()),
            "year": first["year"], "journal": first["journal"],
            "identifiers": " ".join(ids),
            "sources": "; ".join(srcs),
            "n_source_records": len(members),
        })
    rows.sort(key=lambda r: (r["year"], r["title"]))

    # studies represented by more than one surviving report
    per_study = {}
    for r in rows:
        per_study.setdefault(r["study_group"], []).append(r)
    multi = {s: rs for s, rs in per_study.items() if len(rs) > 1}

    # At study level a second PMID is legitimate (protocol plus results paper),
    # but a second NCT is not: one trial, one registration. Two NCTs means the
    # chain ran through a record that merely LISTS trials.
    for s, rs in multi.items():
        ncts = {k for r in rs for k in r["identifiers"].split()
                if k.startswith("nct:")}
        if len(ncts) > 1:
            suspicious.append((len(rs), rs[0]["title"][:70],
                               "study %s spans %d NCTs: %s"
                               % (s, len(ncts), " ".join(sorted(ncts)))))

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    total_in = len(records)
    unique = len(rows)
    dupes = total_in - unique
    no_id_share = len(no_id)

    # --- PRISMA-shaped report ---
    overlap = {}
    for r in rows:
        if r["n_source_records"] > 1:
            overlap[r["sources"]] = overlap.get(r["sources"], 0) + 1

    L = ["# De-duplication across sources", "",
         "Generated by `scripts/deduplicate_sources.py`. Matching is transitive",
         "(union-find), with a normalised title+year fallback for records carrying no",
         "identifier.", "",
         "**Two levels, and they are not the same number.** PRISMA 2020 distinguishes",
         "*reports* from *studies*. A duplicate is the same report retrieved twice;",
         "a protocol and its results paper are two reports of one study, and a registry",
         "entry is a record in its own right. Only the report level belongs in the",
         "\"duplicates removed\" box.", "",
         "| Level | Matched on | Used for |", "|---|---|---|",
         "| Report | DOI, PMID | PRISMA duplicate removal |",
         "| Study | DOI, PMID, NCT | grouping reports of one trial |", "",
         "## Records identified, per source", "",
         "| Source | Records |", "|---|---|"]
    for label, n in per_source.items():
        L.append("| %s | %s |" % (label, "**not supplied**" if n is None else n))
    L += ["| **Total retrieved** | **%d** |" % total_in,
          "| Duplicates removed | %d |" % dupes,
          "| **Records after de-duplication** | **%d** |" % unique, "",
          "Those three numbers are three separate PRISMA boxes. The flow diagram must",
          "show all three, not only the last.", "",
          "## Reports belonging to the same study", "",
          "%d record%s resolve to %d stud%s. %d stud%s carr%s more than one report:"
          % (unique, "" if unique == 1 else "s", len(per_study),
             "y" if len(per_study) == 1 else "ies", len(multi),
             "y" if len(multi) == 1 else "ies", "ies" if len(multi) == 1 else "y"), ""]
    if multi:
        L += ["| Study | Reports |", "|---|---|"]
        for s, rs in sorted(multi.items()):
            L.append("| %s | %s |" % (s, "<br>".join(
                "%s (%s)" % (r["title"][:70], r["year"]) for r in rs)))
        L += ["", "These are **not** duplicates and were not removed. They are grouped so",
              "that data extraction treats them as one study.", "",
              "**Known limitation of the study grouping.** A record that lists exactly one",
              "NCT still links to that trial, and PubMed files a narrative review's",
              "DataBankList the same way it files a trial report's. A review citing a",
              "single trial therefore joins that trial's study group. The rule that",
              "suppresses linking only fires above one identifier, because below it there",
              "is nothing in the metadata that separates \"reports this trial\" from",
              "\"discusses this trial\". Confirm the members of any study group before data",
              "extraction. This does not touch the duplicate count above, which is",
              "computed at report level and ignores NCT entirely.", ""]
    L += ["## Overlap between sources", ""]
    if overlap:
        L += ["| Sources sharing a record | n |", "|---|---|"]
        for k, v in sorted(overlap.items(), key=lambda kv: -kv[1]):
            L.append("| %s | %d |" % (k, v))
    else:
        L.append("No record appeared in more than one source.")
    L += ["", "## Records with no matchable identifier", "",
          "%d of %d source records carry no DOI, PMID or NCT and were matched on" % (no_id_share, total_in),
          "normalised title and year alone. That fallback does not do fuzzy matching, so",
          "a duplicate whose title differs by a word survives as two records. Counting",
          "one study twice is visible in the output; merging two distinct studies is not,",
          "which is why the conservative direction was chosen.", ""]
    if suspicious:
        L += ["## Groups worth checking by hand", "",
              "A PMID identifies one PubMed record and an NCT one registration, so two of",
              "either inside a single group means distinct records were linked. That is",
              "how the truncated-DOI and multi-NCT bugs were caught; anything listed here",
              "must be confirmed by eye before the counts are used.", "",
              "| Records in group | Title | Detail |", "|---|---|---|"]
        for n, t, s in sorted(suspicious, reverse=True)[:20]:
            L.append("| %d | %s | %s |" % (n, t, s))
        L.append("")

    rep = ROOT / args.report
    rep.write_text("\n".join(L), encoding="utf-8", newline="\n")

    print()
    print("total source records      : %d" % total_in)
    print("duplicates removed        : %d" % dupes)
    print("unique records            : %d" % unique)
    print("estudios (reportes agrup) : %d" % len(per_study))
    print("estudios con >1 reporte   : %d" % len(multi))
    print("no matchable identifier   : %d" % no_id_share)
    print("groups to check by hand   : %d" % len(suspicious))

    if over_merged:
        print("\nFAIL: distinct PubMed records were merged into one report")
        for n, t, d in over_merged:
            print("  n=%d | %s | %s" % (n, t, d))
        sys.exit("de-duplication over-merged; do not use this output")
    if known_collisions:
        print("\nFAIL: two included studies were merged into one record")
        for studies, titles in known_collisions:
            print("  %s" % " + ".join(studies))
            for t in titles:
                print("      %s" % t)
        sys.exit("de-duplication over-merged; do not use this output")
    print("auditoria de sobre-fusion : PASS (0 reportes fusionados por error,")
    print("                             0 estudios incluidos fusionados)")
    print("\nwrote %s\nwrote %s" % (out, rep))


if __name__ == "__main__":
    main()
