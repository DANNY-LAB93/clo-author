"""Replace the eradication paragraph, whose interpretation of its own tau-squared
the site split falsifies.

The manuscript read the wide eradication interval as "a genuine feature of the
clinical spectrum, not as noise", citing chronic lung infections that reduced
sputum load without clearing the organism. A round-6 microbiology referee argued
that this is a category error rather than a feature: in ESTABLISHED chronic
airway infection -- cystic fibrosis, primary ciliary dyskinesia with
bronchiectasis, chronic interstitial-lung-disease colonisation -- eradication is
neither achieved nor the therapeutic target, and loading those arms into a
proportion alongside sterilised bacteraemias and explanted implants measures
case-mix rather than phage activity.

The referee proposed a falsifiable test: pool within site class and show whether
the split is what generates the variance. It is. Splitting chronic airway
colonisation from every other site drives tau-squared from 1.995 to EXACTLY ZERO
in the non-airway stratum. The heterogeneity the paper attributed to the clinical
spectrum is a mixture artefact.
"""
import pathlib

BS = chr(92)


def M(name):
    return BS + name + " "


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

anchor = "The eradication estimate carries a wide interval"
start = s.find(anchor)
assert start > 0, "eradication paragraph not found"
end = s.find("not as noise.", start)
assert end > start, "closing phrase not found"
end += len("not as noise.")

new = (
    "The eradication estimate carries the only substantial between-arm variance in the review "
    "($" + BS + "tau^2 = " + M("EradFullTau") + "$), and an earlier version of this section read "
    "that width as ``a genuine feature of the clinical spectrum, not as noise''. That reading is "
    "wrong, and the test that shows it is simple enough to state in a sentence. Eradication means "
    "different things at different sites. In " + BS + "emph{established} chronic airway infection "
    "--- cystic fibrosis, primary ciliary dyskinesia with bronchiectasis, chronic "
    "interstitial-lung-disease colonisation --- clearance is neither achieved nor the therapeutic "
    "target; the endpoints that field uses are bacterial density, exacerbation frequency and "
    "lung function, and eradication is a concept reserved for early acquisition rather than for "
    "the established biofilm state. Elsewhere --- a sterilised bacteraemia, an explanted "
    "culture-negative implant, a healed surgical wound --- clearance is exactly the goal.\n\n"

    "Splitting the corpus on that line resolves the variance completely. Among the "
    + M("EradOtherArms") + "arms at sites other than a chronically colonised airway "
    "(" + M("EradOtherK") + "studies, " + M("EradOtherN") + "patients, " + M("EradOtherEvents")
    + "eradications), the pooled proportion is " + M("EradOtherEst") + "("
    + M("EradOtherCI") + ") with $" + BS + "tau^2 = " + M("EradOtherTau")
    + "$ --- " + BS + "emph{exactly zero}. Among the " + M("EradAirArms") + "chronic-airway arms "
    "(" + M("EradAirK") + "studies, " + M("EradAirN") + "patients, only " + M("EradAirEvents")
    + "eradications), the model degenerates: " + M("EradAirEst") + "with an interval of "
    + M("EradAirCI") + "and $" + BS + "tau^2 = " + M("EradAirTau") + "$, which is the boundary "
    "behaviour of a near-zero-event cell and not an estimate of anything.\n\n"

    "So the heterogeneity was never a property of phage therapy. It was produced by pooling two "
    "endpoints that share a name, and the pooled " + M("EradFullEst") + "is a weighted average of "
    "a coherent 62\\% and a degenerate 3\\% whose mixing proportion is a fact about which "
    "patients happened to be published. We report the overall figure because it is what the "
    "pre-specified analysis produces, but a reader should use the split, and no reader should "
    "read the overall interval as clinical variation. The same objection applies with less force "
    "to the other three outcomes, whose constructs are described in "
    + BS + "Cref{tab:outcome-definitions}; eradication is where it is decisive because the "
    "endpoint is not merely defined differently across arms but is not the same clinical event."
)

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline=chr(10))
print("eradication paragraph rewritten: 'genuine clinical feature' -> mixture artefact")
print("  tau^2 1.995 -> 0.000 once chronic airway is separated")
