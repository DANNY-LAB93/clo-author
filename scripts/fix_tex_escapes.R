# One-off repair of LaTeX escape damage introduced by editing .tex through
# Python/bash heredocs, where "\t" and "\r" in a non-raw string were silently
# converted to a TAB and a carriage return. Two failure modes occurred:
#   \tau^2  -> TAB + "au^2"          (renders as "au^2" in the PDF, no error)
#   \ref{}  -> CR  + "ef{...}"       (renders the literal text "ef{sec:...}")
# LaTeX raises no error for either, so neither is caught by a compile check.
files <- c(
  "paper/main.tex",
  "paper/sections/intro.tex",
  "paper/sections/methods.tex",
  "paper/sections/results.tex",
  "paper/sections/discussion.tex"
)

for (f in files) {
  x <- readLines(f, warn = FALSE)
  before <- paste(x, collapse = "\n")
  s <- before

  # 1. TAB immediately followed by a LaTeX command name fragment -> restore backslash
  s <- gsub("\tau", "\\\\tau", s, fixed = TRUE)
  s <- gsub("\times", "\\\\times", s, fixed = TRUE)
  s <- gsub("\textit", "\\\\textit", s, fixed = TRUE)
  s <- gsub("\textbf", "\\\\textbf", s, fixed = TRUE)
  s <- gsub("\textcite", "\\\\textcite", s, fixed = TRUE)

  # 2. "Section~" (or "(") followed by a line break and a bare "ef{" -> "\ref{"
  s <- gsub("(Section)~[ \t\r\n]*ef\\{", "\\1~\\\\ref{", s)
  s <- gsub("([ (~])[\r\n]*ef\\{sec:", "\\1\\\\ref{sec:", s)
  s <- gsub("(?m)^ef\\{sec:", "\\\\ref{sec:", s, perl = TRUE)

  # 3. any surviving stray control characters
  s <- gsub("\r", "", s, fixed = TRUE)
  s <- gsub("\t", "", s, fixed = TRUE)

  if (!identical(s, before)) {
    writeLines(strsplit(s, "\n", fixed = TRUE)[[1]], f)
    message("repaired: ", f)
  } else {
    message("clean:    ", f)
  }
}
