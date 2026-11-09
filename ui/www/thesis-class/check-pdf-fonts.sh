#!/bin/sh
# usage: check-pdf-fonts.sh <book-dir> <pdf>
#
# Fails the build when the thesis PDF's fonts are not the ones the profile asks
# for. LaTeX does not fail on a missing math font: it falls back to Latin Modern
# Math without an error (apt's Noto Sans Math 2.001 has no OpenType MATH table,
# for one), so look at what the PDF actually embeds. Checks, with poppler's pdffonts:
#   every font is embedded; none is Type 3; Latin Modern Math is absent unless the
#   profile's type.math is latex-default; the profile's main font is present.
# <book-dir> holds _quarto.yml and profiles/ (ui/www or thesis/). The profile is
# thesis.profile in _quarto.yml (default: house). A lighter version of the
# registry's checks (docs/house-class-spec.md, section 7.2, T3).
set -eu
BOOK=$1; PDF=$2
PROFILE=$(sed -n 's/^  profile: *\([A-Za-z0-9_-][A-Za-z0-9_-]*\).*/\1/p' "$BOOK/_quarto.yml" | head -n 1)
PROFILE=${PROFILE:-house}
CFG="$BOOK/profiles/$PROFILE.cfg"
[ -f "$CFG" ] || { echo "::error::no compiled profile $CFG (thesis.profile: $PROFILE)"; exit 1; }
cfgval() { sed -n "s/^\\\\ThesisCfg{$1}{\\(.*\\)}\$/\\1/p" "$CFG" | head -n 1; }
MATH=$(cfgval type.math); MAIN=$(cfgval type.main)
FONTS=$(pdffonts "$PDF" | tail -n +3)
STATUS=0
fail() { echo "::error::$1"; STATUS=1; }

echo "$FONTS" | awk '$(NF-4) != "yes" { bad = 1 } END { exit bad }' \
  || fail "$PDF has a font that is not embedded (see pdffonts)"
echo "$FONTS" | grep -q "Type 3" && fail "$PDF has a Type 3 font (see pdffonts)"
if [ "$MATH" != latex-default ] && echo "$FONTS" | grep -q LatinModernMath; then
  fail "$PDF sets equations in Latin Modern Math, not $MATH. LaTeX fell back silently; check that the math font is installed with an OpenType MATH table."
fi
SQUEEZED_MAIN=$(printf '%s' "$MAIN" | tr -d ' ' | tr 'A-Z' 'a-z')
if [ "$MAIN" != latex-default ] && ! printf '%s' "$FONTS" | tr -d ' ' | tr 'A-Z' 'a-z' | grep -q "$SQUEEZED_MAIN"; then
  fail "$PDF does not use the profile's main font, $MAIN"
fi
[ "$STATUS" = 0 ] && echo "fonts ok for profile $PROFILE (main $MAIN, math $MATH)"
exit $STATUS
