"""Insert the outcome-definitions table into Results, and state the spread.

A round-5 referee wrote: "The definitional range in your own extraction file runs
from Maddocks ('improvement of oxygenation within 3 days with successful
weaning') to Ferry 2022 ('clinical cure at 21 months, with eradication explicitly
discordant'). A 3-day surrogate and a 21-month cure in the same numerator is not
one construct, and no table in the paper lets a reader see this."

The objection was correct and the review's Results already conceded the range in
prose while printing a single percentage. This makes it auditable: every arm's
success definition verbatim, with the longest follow-up horizon its source
states, sorted so the spread is the first thing visible.
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    return BS + name + " "


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

# Anchor: the paragraph that concedes the definitional problem without showing it.
anchor = "Two of these four constructs are less coherent than a single pooled percentage makes them look"
i = s.find(anchor)
assert i > 0, "anchor not found"

para = (
    "The most consequential of those defects is now auditable rather than asserted. "
    + BS + "Cref{tab:outcome-definitions} lists every pooling-eligible arm's clinical-success "
    "definition exactly as recorded from its source, with the longest follow-up horizon that "
    "source states. Only " + M("FollowUpStated") + "of the " + M("ArmsAnalysed") + "arms state a "
    "horizon at all; the other " + M("FollowUpNotStated") + "report success without saying over "
    "what window it was observed. Among those that do, the range runs from "
    + M("FollowUpMin") + "to " + M("FollowUpMax") + ", a " + M("FollowUpFold")
    + "-fold spread. At one end, " + BS + "textcite{Maddocks2019_ajrccm} counts improvement of "
    "oxygenation with successful ventilator weaning; at the other, "
    + BS + "textcite{Arya2026_pji_natcomms} and " + BS + "textcite{Cesta2023_ofid} count absence "
    "of relapse two years after therapy stopped. Both enter the same numerator, weighted "
    "identically. We do not think a single percentage should be read across that range, and the "
    "table is provided so a reader can decide for themselves which arms they are willing to pool. "
    "The table also records what this review still cannot supply: the extraction schema has no "
    "syndrome field, and deriving one by keyword from the recorded text left a quarter of the "
    "arms unclassified and misassigned others, so a syndrome-stratified reading is not available "
    "here (Section~" + BS + "ref{sec:discussion-limitations}).\n\n"
)

s = s[:i] + para + s[i:]

# Place the table float after the paragraph that introduces it.
tbl = (
    "\n\n" + BS + "begin{table}[htbp]\n"
    + BS + "centering\n"
    + BS + "scriptsize\n"
    + BS + "begin{threeparttable}\n"
    + BS + "caption{Clinical-success definitions and follow-up horizons, by study-arm}"
    + BS + "label{tab:outcome-definitions}\n"
    + BS + "input{tables/phage_therapy_mdr_pseudomonas/outcome_definitions_by_arm}\n"
    + BS + "begin{tablenotes}" + BS + "footnotesize\n"
    + BS + "item " + BS + "textit{Notes:} All " + M("ArmsAnalysed") + "pooling-eligible "
    "study-arms. Definitions are reproduced as recorded during extraction from each primary "
    "source, not harmonised. Follow-up is the longest interval the source states within its "
    "success definition; patient ages are excluded from that extraction. "
    + M("FollowUpNotStated") + "arms state no horizon. The spread among those that do is "
    + M("FollowUpMin") + "to " + M("FollowUpMax") + ". This table exists because the pooled "
    "clinical-success proportion in " + BS + "Cref{tab:pooled-estimates} weights every one of "
    "these definitions equally. Source: " + BS + "texttt{scripts/R/15" + BS
    + "_outcome" + BS + "_definitions.R}.\n"
    + BS + "end{tablenotes}\n"
    + BS + "end{threeparttable}\n"
    + BS + "end{table}\n\n"
)

# insert the float at the end of the paragraph block we just added
j = s.find(para) + len(para)
s = s[:j] + tbl + s[j:]

p.write_text(s, encoding="utf-8", newline=chr(10))
print("outcome-definitions paragraph and table inserted")
