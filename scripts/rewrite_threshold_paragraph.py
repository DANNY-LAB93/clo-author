"""Rewrite the threshold-relaxation sentence against the regenerated appendix.

The sentence claimed three sets of newly qualifying cells. Verified against
meta_threshold_relaxation_appendix.tex:

  - "clinical success in the not-classifiable resistance stratum (k=2, N=16)"
    -- that cell is POOLED under the PRIMARY threshold at k=6, N=21. It is not
    a relaxation result at all.
  - "safety and mortality in the topical/local route (k=5, N=18 each)" -- both
    remain NOT_POOLED under the relaxed rule (k=4/N=4 and k=6/N=6).
  - "all four XDR outcome cells (k=4, N=10 each)" -- correct, and now the only
    surviving claim.
  - the parenthetical "(Safety in the inhaled/nebulized route ... now clears the
    primary threshold)" -- it does not; k=3, N=4.

The four DTR "not-derivable" cells, which the appendix previously reported as
newly poolable at k up to 23, are now marked NOT_ELIGIBLE: they were excluded on
definitional grounds that no threshold change can address (05_robustness.R).
That exclusion is stated here because a reader is entitled to know the appendix
declines to answer a question rather than having found nothing.
"""
import pathlib

BS = chr(92)


def M(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

start = s.find("An appendix-only relaxation of the threshold to at least 2 studies and 10 patients")
assert start > 0, "threshold paragraph anchor not found"
tail_anchor = "These estimates are reported only to show that the primary threshold is itself consequential"
end = s.find(tail_anchor)
assert end > start, "tail anchor not found"

new = (
    "An appendix-only relaxation of the threshold to at least 2 studies and 10 patients ("
    + BS + "Cref{tab:threshold-relaxation}) qualifies " + M("RelaxNewlyPoolable")
    + " further cells, and they are all the same stratum: the four XDR outcome cells, each at "
    "$k=" + M("CsResXDRK") + "$ and $N=" + M("CsResXDRN") + "$, having just reached the "
    "ten-patient relaxed floor as the corpus grew. Nothing else moves. PDR, intravenous, "
    "topical/local and inhaled/nebulized remain below even the relaxed threshold for every "
    "outcome. Earlier versions of this paragraph also named not-classifiable clinical success "
    "and two topical/local cells as newly qualifying; the first is pooled under the "
    + BS + "emph{primary} threshold and was never a relaxation result, and the second two do not "
    "qualify under either rule.\n\n"

    "The four DTR ``not-derivable'' cells are excluded from this appendix rather than relaxed "
    "into it, and the reason matters more than the exclusion. A threshold states how much "
    "evidence is enough, so relaxing one can only rescue a cell that failed for want of "
    "evidence. That cell did not: it is not fitted at all "
    "(Section~" + BS + "ref{sec:methods-estimation}) because a proportion computed over arms "
    "whose difficult-to-treat status is unknown describes no definable population, and no sample "
    "size repairs that. An earlier version of this appendix pooled those four cells anyway and "
    "reported them as newly poolable at $k$ up to 23 --- which would have told a reader that a "
    "larger corpus rescues the DTR analysis. It does not, and the two scripts now agree. "
    )

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline="\n")
print("threshold-relaxation passage rewritten (" + str(len(new)) + " chars)")
