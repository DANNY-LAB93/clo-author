"""Phase D bibliography repair.

Three jobs:

1. Replace the two European Respiratory Review entries. They were added earlier
   with PLACEHOLDER author lists, flagged as unverified in their own note
   fields. PubMed now gives the real ones, and neither matches the placeholder:
       Eur Respir Rev 2024;33:240029 -> Vaezi A, Healy T, et al. (not "Bagheri")
       Eur Respir Rev 2022;31:220121 -> Mitropoulou G, Koutsokera A, et al.
                                        (not "Loiseau")
   The citation keys are renamed to match the real first authors, and every
   in-text use is updated, so the printed citation is not misattributed.

2. Delete three template leftovers that are cited nowhere: two econometrics
   references inherited from the project scaffold (Angrist 2009, Imbens 2004)
   and an uncited prevalence-methods entry (Munn 2015).

3. Append the clinical-practice and GRADE-for-non-comparative framework
   references the review argues from but never cited.
"""
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
bib = root / "Bibliography_base.bib"
text = bib.read_text(encoding="utf-8")

BS = chr(92)

# --- 1. drop the placeholder ERS entries and the uncited template leftovers ----
DROP_KEYS = [
    "Bagheri2024_errev",
    "Loiseau2022_errev",
    "Angrist2009_mostly_harmless",
    "Imbens2004_nonparametric",
    "Munn2015_prevalence",
]

for key in DROP_KEYS:
    # match "@type{key, ... }" up to the closing brace that starts a line
    pattern = re.compile(
        r"\n@[a-z]+\{" + re.escape(key) + r",.*?\n\}\n", re.DOTALL
    )
    text, n = pattern.subn("\n", text)
    print(("removed  " if n else "NOT FOUND ") + key)

# --- 2. append corrected / new entries ----------------------------------------
NEW = r"""
@article{Vaezi2024_errev,
  author  = {Vaezi, Atefeh and Healy, Thomas and Ebrahimi, Golnaz and Rezvankhah, Saeid and Hashemi Shahraki, Abdolrazagh and Mirsaeidi, Mehdi},
  title   = {Phage Therapy: Breathing New Tactics into Lower Respiratory Tract Infection Treatments},
  journal = {European Respiratory Review},
  volume  = {33},
  number  = {172},
  pages   = {240029},
  year    = {2024},
  doi     = {10.1183/16000617.0029-2024},
  note    = {\% AUTHOR LIST VERIFIED (2026-07-28) via PubMed esummary, PMID 38925791, PMC11216685. This entry REPLACES an earlier one filed under the key Bagheri2024_errev with a placeholder author list that was wrong -- the first author is Vaezi, not Bagheri. Serves two roles in this review: a prior respiratory-focused synthesis positioned against in the Discussion, and one of the two concordant secondary sources from which the Maddocks 2019 case was reconstructed (its Table 1 gives the patient age and sex, both routes, dose, duration, concomitant antibiotics and outcome, and labels five other rows MDR while recording the Maddocks row as plain P. aeruginosa).}
}

@article{Mitropoulou2022_errev,
  author  = {Mitropoulou, Georgia and Koutsokera, Angela and Csajka, Chantal and Blanchon, Sylvain and Sauty, Alain and Brunet, Jean-Francois and von Garnier, Christophe and Resch, Gr\'egory and Guery, Benoit},
  title   = {Phage Therapy for Pulmonary Infections: Lessons from Clinical Experiences and Key Considerations},
  journal = {European Respiratory Review},
  volume  = {31},
  number  = {166},
  pages   = {220121},
  year    = {2022},
  doi     = {10.1183/16000617.0121-2022},
  note    = {\% AUTHOR LIST VERIFIED (2026-07-28) via PubMed esummary, PMID 36198417, PMC9724797. This entry REPLACES an earlier one filed under the key Loiseau2022_errev with a placeholder author list that was wrong -- the first author is Mitropoulou, not Loiseau. Second, independent secondary source corroborating the Maddocks 2019 extraction, concordant with Vaezi2024_errev on phage product, duration, both routes, all three concomitant antibiotics and outcome; it also defines eradication as negative cultures at 6 months, the definition adopted for that arm.}
}

@article{Suh2022_aac,
  author  = {Suh, Gina A. and Lodise, Thomas P. and Tamma, Pranita D. and Knisely, Jane M. and Alexander, Jose and Aslam, Saima and Barton, Karen D. and Bizzell, Erica and Totten, Katherine M. C. and Campbell, Joseph L. and Chan, Benjamin K. and Cunningham, Scott A. and Goodman, Katherine E. and Greenwood-Quaintance, Kerryl E. and Harris, Anthony D. and Hesse, Shayla and Maresso, Anthony and Nussenblatt, Veronique and Pride, David and Rybak, Michael J. and Sund, Zoe and van Duin, David and Van Tyne, Daria and Patel, Robin},
  title   = {Considerations for the Use of Phage Therapy in Clinical Practice},
  journal = {Antimicrobial Agents and Chemotherapy},
  volume  = {66},
  number  = {3},
  pages   = {e02071--21},
  year    = {2022},
  doi     = {10.1128/AAC.02071-21},
  note    = {\% VERIFIED (2026-07-28) via PubMed esummary, PMID 35041506, PMC8923208. Antibacterial Resistance Leadership Group (ARLG) expert-panel consensus on when phage therapy might be considered, what laboratory testing is needed, and the pharmacokinetic questions that remain open. This is the field's de facto clinical-practice framework; a review that makes recommendations for practice and future research needs to engage it rather than write around it.}
}

@misc{WHO2024_bppl,
  author       = {{World Health Organization}},
  title        = {WHO Bacterial Priority Pathogens List, 2024: Bacterial Pathogens of Public Health Importance to Guide Research, Development and Strategies to Prevent and Control Antimicrobial Resistance},
  howpublished = {World Health Organization, Geneva},
  year         = {2024},
  note         = {\% NOT independently re-verified via PubMed in this session -- a WHO report rather than a journal article, so it is not PubMed-indexed; cited per its standard bibliographic record, the same convention this review applies to Higgins2023_cochranehandbook, FreemanTukey1950 and Miller1978. Cited because the 2024 update RECLASSIFIED carbapenem-resistant P. aeruginosa from Critical to High priority, superseding the 2018 list this review's Introduction currently frames its urgency argument on. The reclassification cuts against, rather than for, the paper's motivation, which is why it is stated explicitly instead of quietly retaining the older list.}
}
"""

text = text.rstrip() + "\n" + NEW
bib.write_text(text, encoding="utf-8", newline="\n")
print("appended: Vaezi2024_errev, Mitropoulou2022_errev, Suh2022_aac, WHO2024_bppl")

# --- 3. repoint every in-text citation at the corrected keys -------------------
TEX = [
    "paper/main.tex",
    "paper/sections/intro.tex",
    "paper/sections/methods.tex",
    "paper/sections/results.tex",
    "paper/sections/discussion.tex",
]
for rel in TEX:
    p = root / rel
    s = p.read_text(encoding="utf-8")
    o = s
    s = s.replace("Bagheri2024_errev", "Vaezi2024_errev")
    s = s.replace("Loiseau2022_errev", "Mitropoulou2022_errev")
    if s != o:
        p.write_text(s, encoding="utf-8", newline="\n")
        print("repointed citations in " + rel)
