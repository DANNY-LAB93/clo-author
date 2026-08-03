"""Enumerate the local document corpus and resolve each file to an identifier.

WHY THIS EXISTS. The manuscript names a local PDF corpus as a PRISMA
identification channel contributing eight records, and the folder it refers to
carries no record of what is in it or where any of it came from. A channel whose
contents cannot be enumerated cannot be re-screened, by a referee or by the
authors, and that is a reproducibility failure rather than the declared
methodological limitation it is currently presented as (PRISMA 2020 items 6-7).

WHAT THIS DOES. Walks the corpus folders, resolves every PDF to a DOI, PMID or
PMC id where one can be recovered, and matches it against
quality_reports/corpus_identifier_index.txt. Output is one row per file.

IDENTIFIER RECOVERY, in order of reliability:
  1. the file name, when it already carries an identifier (the PMC download
     manifest names files PMCxxxxxxx.pdf);
  2. PDF document metadata (/Subject and /Title frequently carry the DOI);
  3. the text of page 1, which is where journals print the DOI.
Page 1 only: the reference list of any phage paper cites dozens of DOIs, and
scanning the whole document would attribute other people's identifiers to this
file. This is the same reasoning that rules out Ovid's .mp. field.

WHAT IT DELIBERATELY DOES NOT DO. It does not decide eligibility and it does not
reconstruct screening decisions. A file appearing here is a file that was
present, not a record that was screened -- those are different claims and the
distinction is what the manuscript currently blurs.

USAGE
    python scripts/build_document_corpus_manifest.py "C:/Users/Equipo/Desktop/opcion 1"
"""
import csv
import hashlib
import pathlib
import re
import sys
import warnings

warnings.filterwarnings("ignore")

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "quality_reports" / "corpus_identifier_index.txt"
OUT_CSV = ROOT / "data" / "raw" / "document_corpus_manifest.csv"

DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s,;)}\]\"'<>]+)")
PMID_RE = re.compile(r"PMID[:\s]*(\d{7,8})", re.I)
PMC_RE = re.compile(r"(PMC\d{6,8})", re.I)


def norm_doi(d):
    return re.sub(r"[.,;:)\]]+$", "", d).lower()


def ids_from(text):
    out = []
    for d in DOI_RE.findall(text or ""):
        out.append("doi:" + norm_doi(d))
    for p in PMID_RE.findall(text or ""):
        out.append("pmid:" + p)
    for p in PMC_RE.findall(text or ""):
        out.append("pmc:" + p[3:])
    return list(dict.fromkeys(out))


def first_page_text(path):
    try:
        import pdfplumber
        with pdfplumber.open(str(path)) as pdf:
            if not pdf.pages:
                return "", {}
            txt = pdf.pages[0].extract_text() or ""
            meta = pdf.metadata or {}
            return txt, meta
    except Exception as e:
        return "", {"__error__": type(e).__name__}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    base = pathlib.Path(sys.argv[1])
    if not base.exists():
        sys.exit("corpus root not found: %s" % base)

    corpus = {}
    if INDEX.exists():
        for line in INDEX.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                ident, _, sid = line.partition("\t")
                corpus[ident.strip().lower()] = sid.strip()

    # The PMC download manifest is the only true provenance artefact in the
    # corpus: it records the URL each file was fetched from.
    pmc_manifest = {}
    html = base / "Descargar_PDFs.html"
    if html.exists():
        for m in re.finditer(
                r"href='([^']+)'\s+download='([^']+)'", html.read_text(encoding="utf-8", errors="replace")):
            pmc_manifest[m.group(2)] = m.group(1)

    pdfs = sorted(base.rglob("*.pdf"))
    print("folders under %s" % base)
    for d in sorted({p.parent for p in pdfs}):
        print("   %4d  %s" % (len(list(d.glob("*.pdf"))), d.relative_to(base)))
    print("\nresolving %d files (page 1 only)...\n" % len(pdfs))

    rows = []
    for i, p in enumerate(pdfs, 1):
        if i % 25 == 0:
            print("   %d/%d" % (i, len(pdfs)), flush=True)
        found = ids_from(p.name)
        source = "filename" if found else ""
        meta_txt = ""
        if not found:
            txt, meta = first_page_text(p)
            meta_txt = " ".join(str(v) for v in meta.values() if v)
            found = ids_from(meta_txt)
            source = "pdf-metadata" if found else source
            if not found:
                found = ids_from(txt)
                source = "page-1-text" if found else "unresolved"

        hit = next((corpus[i_] for i_ in found if i_ in corpus), "")
        rows.append({
            "folder": p.parent.relative_to(base).as_posix(),
            "filename": p.name,
            "size_bytes": p.stat().st_size,
            "sha1_16": hashlib.sha1(p.read_bytes()).hexdigest()[:16],
            "identifiers": " ".join(found),
            "id_source": source,
            "download_url": pmc_manifest.get(p.name, ""),
            "in_corpus_as": hit,
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    resolved = sum(1 for r in rows if r["identifiers"])
    matched = sum(1 for r in rows if r["in_corpus_as"])
    studies = {r["in_corpus_as"] for r in rows if r["in_corpus_as"]}
    print("\nfiles                       : %d" % len(rows))
    print("resolved to an identifier   : %d" % resolved)
    print("unresolved                  : %d" % (len(rows) - resolved))
    print("matching an included study  : %d files -> %d distinct studies of %d"
          % (matched, len(studies), len(set(corpus.values()))))
    print("with a recorded download URL: %d" % sum(1 for r in rows if r["download_url"]))
    print("\nwrote", OUT_CSV)


if __name__ == "__main__":
    main()
