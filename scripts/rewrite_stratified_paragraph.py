"""Replace the stratified-results paragraph in Results.

The paragraph being replaced reported three outcome-stratum cells as pooled --
not-classifiable safety, not-classifiable mortality, and inhaled/nebulized
safety -- each with a point estimate, a confidence interval and a patient
denominator. None of the three ever met the pooling threshold, and none of
those numbers appears in any pipeline output. It also reported all four
route-"other" estimates and the MDR eradication estimate at values from a
superseded corpus, and asserted a Clopper-Pearson bound computed for a
denominator this corpus does not have.

The replacement quotes no numeric literal. Every estimate, interval, study
count and patient count resolves through a macro emitted by
scripts/R/13_tex_macros.R, which writes macros only for cells the pipeline
actually pooled. A cell that stops pooling therefore deletes its own macros and
breaks the build rather than leaving a stale number in the prose.

Written as a file rather than a heredoc because backslash sequences in a
non-raw Python string have corrupted these .tex files three times.
"""
import pathlib

BS = chr(92)


def cmd(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

anchor = "Four stratified categories reached the threshold for at least one outcome."
start = s.find(anchor)
assert start > 0, "anchor paragraph not found"
end = s.find("\n", start)
assert end > start

new = (
    "Four stratified cells reached the threshold, and two of the four are residual categories "
    "rather than clinical classes --- a fact that shapes how much any of this can be relied on. "
    "The clearest positive result is a genuine resistance class: the "
    + cmd("textbf") + "{MDR stratum is pooled across all four outcomes} --- clinical success "
    + cmd("CsResMDREstCI") + " (" + cmd("CsResMDRK") + " studies, " + cmd("CsResMDRN")
    + " patients; " + cmd("Cref") + "{fig:forest-success-mdr}), safety " + cmd("SafResMDREstCI")
    + " (" + cmd("SafResMDRK") + " studies, " + cmd("SafResMDRN") + " patients), eradication "
    + cmd("EradResMDREstCI") + " (" + cmd("EradResMDRK") + " studies, " + cmd("EradResMDRN")
    + " patients), and mortality " + cmd("MortResMDREstCI") + " (" + cmd("MortResMDRK")
    + " studies, " + cmd("MortResMDRN") + " patients). This answers part of the review's "
    "originally-blocked core stratification aim --- an MDR-specific pooled estimate now exists "
    "--- but only as a fragile, single-cohort signal: " + cmd("citeauthor")
    + "{Pirnay2024_natmicrobiol} still supplies roughly three-fifths of the MDR clinical-success "
    "patients, and the estimate clears the threshold only under author-reported resistance "
    "labels, collapsing to three studies and four patients when classification is restricted to "
    "independently verified cases (Section~" + cmd("ref") + "{sec:results-robustness}).\n\n"

    "It does not complete the aim as designed. " + cmd("textbf") + "{XDR ("
    + cmd("CsResXDRK") + " studies, " + cmd("CsResXDRN") + " patients) and PDR ("
    + cmd("CsResPDRK") + " studies, " + cmd("CsResPDRN") + " patients) remain below the "
    "20-patient threshold for every outcome} and are reported in " + cmd("Cref")
    + "{tab:not-pooled} as insufficient evidence, so the MDR-" + cmd("emph") + "{versus}-XDR "
    "comparison this review was designed to make still cannot be made, even though MDR alone can "
    "now be estimated.\n\n"

    "Exactly one further resistance cell pools, and it is the most uncomfortable number in this "
    "review. Clinical success in the not-classifiable stratum is " + cmd("CsResNotClassifiableEstCI")
    + " across " + cmd("CsResNotClassifiableK") + " studies and " + cmd("CsResNotClassifiableN")
    + " patients --- the " + cmd("emph") + "{highest} point estimate anywhere in the review, in "
    "the one stratum defined by the " + cmd("emph") + "{absence} of resistance documentation. We "
    "do not read this as evidence that undocumented infections respond better. Two readings "
    "cannot be separated with these data: reports that omit an antibiogram may be systematically "
    "the ones with favourable outcomes, or the stratum may simply contain less-resistant patients "
    "whom the eligibility rule admitted. The first is reporting bias and the second is a defect "
    "in this review's own inclusion criterion; neither is reassuring, and "
    "Section~" + cmd("ref") + "{sec:discussion-limitations} treats them as the review's central "
    "threat rather than as a caveat.\n\n"

    "The remaining two not-classifiable cells do " + cmd("emph") + "{not} pool. Safety reaches "
    "only " + cmd("SafResNotClassifiableK") + " studies and " + cmd("SafResNotClassifiableN")
    + " patients; mortality " + cmd("MortResNotClassifiableK") + " studies and "
    + cmd("MortResNotClassifiableN") + " patients. Earlier drafts of this section reported both "
    "as pooled, with point estimates and confidence intervals. Those cells never met the "
    "threshold and those numbers had no counterpart in any pipeline output. They are withdrawn, "
    "and Section~" + cmd("ref") + "{sec:discussion-limitations} records how they survived four "
    "rounds of review, because that failure is itself a finding about this manuscript.\n\n"

    "On the route axis, the multi-route or otherwise unclassifiable (``other'') category is "
    "pooled across all four outcomes: clinical success " + cmd("CsRouteOtherEstCI") + " ("
    + cmd("CsRouteOtherK") + " studies, " + cmd("CsRouteOtherN") + " patients), safety "
    + cmd("SafRouteOtherEstCI") + " (" + cmd("SafRouteOtherK") + " studies, "
    + cmd("SafRouteOtherN") + " patients), eradication " + cmd("EradRouteOtherEstCI") + " ("
    + cmd("EradRouteOtherK") + " studies, " + cmd("EradRouteOtherN") + " patients), and mortality "
    + cmd("MortRouteOtherEstCI") + " (" + cmd("MortRouteOtherK") + " studies, "
    + cmd("MortRouteOtherN") + " patients). " + cmd("textbf") + "{No specific single route "
    "reaches the threshold for any outcome.} Inhaled/nebulized comes closest on study count and "
    "still falls far short on patients: its safety cell holds "
    + cmd("SafRouteInhaledNebulizedK") + " studies and " + cmd("SafRouteInhaledNebulizedN")
    + " patients. Where a route records no deaths at all we report an exact one-sided "
    "(Clopper-Pearson) bound rather than a pooled zero, since a pooled 0.0" + cmd("%")
    + " with an interval spanning the whole range conveys nothing: inhaled/nebulized has 0 deaths "
    "among " + cmd("MortZeroInhaledNebulizedN") + " patients (97.5" + cmd("%") + " upper bound "
    + cmd("MortZeroInhaledNebulizedCPupper") + "), and topical/local 0 among "
    + cmd("MortZeroTopicalLocalN") + " (upper bound " + cmd("MortZeroTopicalLocalCPupper")
    + "). Both bounds are consistent with mortality as high as roughly one patient in four, and "
    "neither supports any claim of route-specific safety.\n\n"

    "Modality could not be stratified at all. " + cmd("ModPhageMonotherapyArms") + " of the "
    + cmd("ArmsAnalysed") + " arms is phage monotherapy (" + cmd("textcite")
    + "{Arya2026_pji_natcomms}, one patient) and the other "
    + cmd("ModPhageAntibioticCombinationArms") + " combine phage with antibiotics, so there is no "
    "antibiotic-monotherapy stratum to compare against and no poolable phage-monotherapy stratum "
    "either (" + cmd("Cref") + "{tab:not-pooled}, final row). This is the cleanest single "
    "statement of what the corpus cannot answer: with one exception the published record does not "
    "contain a patient given phage without a concomitant antibiotic, so no arm in this synthesis "
    "can attribute its outcome to the phage."
)

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline="\n")
print("stratified paragraph rewritten (" + str(len(new)) + " chars, 0 numeric literals)")
