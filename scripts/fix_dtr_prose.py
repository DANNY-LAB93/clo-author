"""Correct the DTR definition wherever the manuscript states it, and rewrite the
finding that the mis-statement produced.

Kadri et al. 2018 (Clin Infect Dis 67:1803-1814) define DTR in their Methods as
"intermediate or resistant to all reported agents in carbapenem, beta-lactam, and
fluoroquinolone categories", framed throughout as loss of all FIRST-LINE agents,
with aminoglycosides, polymyxins and tigecycline named as the RESERVE agents a
DTR patient is forced onto. Reserve agents do not enter the determination.

This manuscript said "every beta-lactam and every fluoroquinolone" and "all
beta-lactams and all fluoroquinolones". That is stricter than Kadri: it pulls
reserve and post-2018 agents into the requirement. The consequence was not
cosmetic -- the review manufactured part of the non-derivability it then reported
as its headline DTR finding, and produced a coding scheme in which no arm could
ever be shown DTR-NEGATIVE.

Re-adjudicating against the correct criterion moved six arms and made the
negative level reachable for the first time.
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    return BS + name + " "


root = pathlib.Path(__file__).resolve().parent.parent
failures = []


def swap(fname, old, new, note):
    p = root / "paper" / "sections" / fname
    s = p.read_text(encoding="utf-8")
    if s.count(old) != 1:
        failures.append("%s :: %s (matches %d)" % (fname, note, s.count(old)))
        return
    p.write_text(s.replace(old, new, 1), encoding="utf-8", newline=chr(10))
    print("  ok   " + note)


# ---- Introduction -----------------------------------------------------------
swap("intro.tex",
     BS + "textcite{Kadri2018_dtr} instead define " + BS + "emph{difficult-to-treat "
     "resistance} (DTR) as non-susceptibility to " + BS + "emph{all} first-line agents --- "
     "every $" + BS + "beta$-lactam and every fluoroquinolone --- which is the point at which a "
     "clinician is forced onto reserve therapy.",

     BS + "textcite{Kadri2018_dtr} instead define " + BS + "emph{difficult-to-treat resistance} "
     "(DTR) as non-susceptibility to all " + BS + "emph{first-line} agents --- the carbapenem, "
     "extended-spectrum cephalosporin, $" + BS + "beta$-lactam/$" + BS + "beta$-lactamase-inhibitor "
     "and fluoroquinolone categories --- which is the point at which a clinician is forced onto "
     "reserve therapy. The reserve agents themselves, which "
     + BS + "citeauthor{Kadri2018_dtr} name as aminoglycosides, polymyxins and tigecycline, do "
     + BS + "emph{not} enter the determination: an isolate susceptible only to colistin is DTR "
     "precisely because colistin is what is left.",
     "Introduction: DTR defined by first-line categories, reserve agents excluded")

# ---- Methods ----------------------------------------------------------------
swap("methods.tex",
     "A " + BS + "emph{fourth} stratification axis records difficult-to-treat resistance "
     + BS + "parencite{Kadri2018_dtr}, defined as non-susceptibility to all $" + BS
     + "beta$-lactams and all fluoroquinolones.",

     "A " + BS + "emph{fourth} stratification axis records difficult-to-treat resistance "
     + BS + "parencite{Kadri2018_dtr}, defined as intermediate or resistant status to all "
     "reported first-line agents --- carbapenems, extended-spectrum cephalosporins, $"
     + BS + "beta$-lactam/$" + BS + "beta$-lactamase-inhibitor combinations and fluoroquinolones. "
     "Aminoglycosides, polymyxins and tigecycline are reserve agents in "
     + BS + "citeauthor{Kadri2018_dtr}'s scheme and are excluded from the determination, as are "
     "agents postdating it (ceftazidime-avibactam, ceftolozane-tazobactam, cefiderocol), which "
     + BS + "citeauthor{Kadri2018_dtr} note a future revision would need to address. Two "
     "consequences follow and both are applied here: an isolate susceptible only to reserve "
     "agents is DTR-" + BS + "emph{positive}, and a single documented susceptible first-line "
     "agent is sufficient to establish DTR-" + BS + "emph{negative}. Earlier rounds of this "
     "review required non-susceptibility to " + BS + "emph{all} $" + BS + "beta$-lactams, which "
     "is stricter than " + BS + "citeauthor{Kadri2018_dtr} and under which no arm could be shown "
     "negative; six arms were re-adjudicated when the criterion was corrected.",
     "Methods: DTR criterion corrected, with both directions of adjudication stated")

if failures:
    print("")
    print("NOT APPLIED:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("")
print("DTR definition corrected in Introduction and Methods")
