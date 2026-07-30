"""Rewrite the phage-resistance passage, whose numbers were wrong by a factor of
four and whose interpretation the correction inverts.

The passage read: "Only [9] of the [40] pooling-eligible arms record this outcome
at all -- Liu 2025's retained PDR patient, Aslam 2019's Patient 1, Kohler 2023,
and Li 2025 -- covering 4 patients, of whom 1 developed phage resistance during
therapy. ... The more informative observation is the reporting rate itself."

Three things were wrong. The named list had four arms while the macro said nine.
The event count was one when the dataset holds four. And Yang 2025 carried
resistance_emergence_n = NA while its own extraction note recorded that the load
was reduced but not eradicated "as phage-resistant strains emerged" -- a
documented event coded missing, now corrected.

The interpretation changes with the arithmetic. "1 of 4" supports the review's
framing that the reporting rate is the story. Four events among nine arms that
assessed it says something different and more important: where investigators
looked for phage resistance, they found it about half the time. That is a
statement about phage therapy, not about publication practice, and this review
was sitting on it.
"""
import pathlib

BS = chr(92)


def M(name):
    return BS + name + " "


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

start = s.find(BS + "textbf{Emergence of phage resistance during treatment.}")
assert start > 0, "phage-resistance passage not found"
end = s.find(BS + "textbf{", start + 10)
if end < 0:
    end = s.find("\n", start)
assert end > start

new = (
    BS + "textbf{Emergence of phage resistance during treatment.} "
    + M("ResistEmergenceReported") + "of the " + M("ArmsAnalysed") + "pooling-eligible arms "
    "assess this outcome, and " + M("ResistEmergenceEvents") + "of those "
    + M("ResistEmergenceReported") + " --- " + M("ResistEmergenceEventPct") + " --- document "
    "phage resistance emerging during therapy. No pooled proportion is defensible from a "
    "denominator of " + M("ResistEmergenceReported") + ", and none is offered, but the ratio "
    "should not be buried: " + BS + "emph{where investigators looked, they found it about half "
    "the time.} The documented mechanisms differ and are worth separating. "
    + BS + "textcite{Li2025_hlife_biliary} records O-antigen-deficient escape mutants arising "
    "under a four-phage cocktail, forcing a switch to a double-stranded RNA phage --- receptor "
    "loss, the canonical route. " + BS + "textcite{Zaldastanishvili2021_viruses} documents "
    "population diversification by pulsed-field gel electrophoresis across serial isolates in "
    "both patients, with susceptibility differing between co-existing strains rather than being "
    "lost outright. " + BS + "textcite{Yang2025_scirep} records emergence as the reason the "
    "bacterial load fell without the organism being eradicated. Running the other way, "
    + BS + "textcite{Chan2018_omko1_emph} is the case in which phage pressure "
    + BS + "emph{restored} antibiotic susceptibility through the efflux-pump trade-off that "
    "motivates phage steering.\n\n"

    "The reporting rate remains the second finding rather than the first: "
    + M("ResistEmergenceSilent") + "of " + M("ArmsAnalysed") + "arms are silent on whether the "
    "organism became phage-resistant, so this review cannot say how often it happens --- only "
    "that among the minority who checked, it happened often. An earlier version of this section "
    "reported one event among four arms and treated the reporting rate as the whole story. That "
    "understated the events by a factor of four, and one of the four "
    "(" + BS + "citeauthor{Yang2025_scirep}) had been coded as not assessed although its own "
    "source describes the emergence explicitly.\n\n"
)

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline=chr(10))
print("phage-resistance passage rewritten: 1-in-4 becomes 4-in-9, with mechanisms separated")
