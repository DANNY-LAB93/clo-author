"""Extend the round-5 selection narrative to the second, un-blocked search pass.

The narrative written after the first pass said "three arms across two studies
were added ... all three are eradication failures, and pooled eradication fell by
more than seven percentage points". That was accurate then. The second pass --
the un-blocked search the methods referee demanded -- added four more arms with
mixed outcomes, so both the count and the directional claim need replacing.
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    return BS + name + " "


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

start = s.find("Three arms across two studies were added, and the consequence is reported")
assert start > 0, "first-pass closing sentence not found"
end_marker = "complete."
end = s.find(end_marker, start)
assert end > start, "closing anchor not found"
end += len(end_marker)

new = (
    "Two eligible studies came out of that batch --- " + BS + "textcite{Zaldastanishvili2021_viruses} "
    "with two arms and " + BS + "textcite{Green2023_cid} with one --- and all three arms are "
    + BS + "emph{eradication failures}.\n\n"

    "That result made the referee's second demand unavoidable, and it carried a falsifiable "
    "bar: re-run the search with the resistance block removed, and if it yields two or fewer "
    "new eligible studies, accept that the corpus is near-complete. We ran it. PubMed as "
    "title/abstract " + BS + "textit{Pseudomonas aeruginosa} with phage-therapy terms, restricted "
    "to clinical publication types and 2016--2026, returned 45 records: 17 already traceable to "
    "this corpus and 28 never screened. The bar was not met. Seven of the 28 entered the "
    "analytic dataset, and the outcome of each is reported rather than summarised.\n\n"

    "Four are pooled. " + BS + "textcite{Casazza2025_otolneurotol}, chronic mastoiditis from an "
    "MDR strain in a lung-transplant recipient, is the only one that achieved eradication. "
    + BS + "textcite{Teney2024_viruses}, four successive episodes of ventilator-associated "
    "pneumonia in a patient with burns over 81\\% of the body surface, did not: its conclusion "
    "states verbatim that phage-antibiotic synergy ``did not result in microbial success'' while "
    "the clinical outcome was favourable. " + BS + "textcite{Li2023_microbiotechnol}, the "
    "first-in-human use of a double-stranded RNA phage, did not either --- the paper carries a "
    "passage headed ``reasons for the failure to completely eradicate'' --- and it contributes "
    "only the second phage-attributable adverse event in this review, a fever to 38.7\\degree C "
    "after every course. " + BS + "textcite{Chen2022_bst}, a post-pneumonectomy empyema, cleared "
    "its pathogen.\n\n"

    "Three were extracted and then excluded, each by a rule already in force, and naming them "
    "matters more than counting them. " + BS + "textcite{Chung2026_natcommun} and "
    + BS + "textcite{Ronit2024_ugeskr} fail the population criterion on their own published "
    "antibiograms: the first isolate was merely intermediate to ciprofloxacin and susceptible to "
    "piperacillin-tazobactam, ceftazidime-avibactam and meropenem; the second was resistant to "
    "two agents and susceptible to meropenem and ciprofloxacin. Neither reaches "
    + BS + "textcite{Magiorakos2012_mdr}'s three-category threshold, and neither paper claims it "
    "does --- the same ground on which " + BS + "citeauthor{Liu2025_mlife_perinephric}'s first "
    "patient was excluded. " + BS + "textcite{Jennes2017_critcare} is the harder case and the more "
    "instructive one: it is the study the referee named as unfindable by any query requiring a "
    "resistance keyword, since its title says ``colistin-only-sensitive'' rather than XDR, and it "
    "would have been this review's fourth phage-monotherapy arm and a death. It is excluded as a "
    "probable duplicate of a patient inside the " + BS + "citeauthor{Pirnay2024_natmicrobiol} "
    "roster, on the same rule applied to " + BS + "citeauthor{Ferry2022_natcomms} and "
    + BS + "citeauthor{Racenis2023_viruses}, and is restored in the de-duplication sensitivity "
    "analysis.\n\n"

    "The honest summary of both passes is not that the corpus is now complete. It is that a "
    "search this review had called ``materially improved'' surfaced seven previously unscreened "
    "eligible or extractable records as soon as one keyword was dropped, that the referees' "
    "diagnosis of the cause was exactly right, and that the resistance-blocked queries reported "
    "in Section~" + BS + "ref{sec:methods-search} should be read as a lower bound on what the "
    "published record contains."
)

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline=chr(10))
print("second-pass narrative written (" + str(len(new)) + " chars)")
print("  four new studies cited; three exclusions named with their grounds")
