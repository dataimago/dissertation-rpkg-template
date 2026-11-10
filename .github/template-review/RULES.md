# Review rules - dissertation-rpkg-template

Review the PR diff for changed-code correctness, security, regressions, and
violations of the contracts below. This repo is a **GitHub template**: the
dissertation-ai hub creates every author's R-package repository from it, so a
defect here is copied into every dissertation. Report concrete, actionable
defects; do not turn style preferences or speculative redesigns into findings.
Severity: P1 blocks the PR; P2 should be fixed; P3 is optional.

## P1 - every generated repo inherits this file

- **Placeholders stay intact.** Mustache variables (`{{user.name}}`,
  `{{rPackage.name}}`, `{{rPackage.rName}}`, `{{thesis.workingTitle}}`,
  `{{user.githubUsername}}`, `{{metadata.name}}` and the like) in `DESCRIPTION`,
  `README.md`, `ui/www/_quarto.yml` and the chapters must not be removed,
  renamed, hard-coded or broken (`{ {`, a stray brace). A new placeholder needs
  the hub to know it: say so.
- **Nothing is specific to one author.** No real name, institution, thesis
  title, GitHub handle or e-mail in a file the hub copies. The CU Boulder
  values in `THESIS-CLS-README.md` are examples of a registry entry only.
- **No secrets, no real manuscript prose.** Chapter starters, tests and
  examples are synthetic. Report an exposure without quoting the value.
- **Template-only files stay template-only.** `composer-review.yml` and
  `.github/template-review/` must keep the
  `github.repository == 'dataimago/dissertation-rpkg-template'` guard on every
  job, and must not move under `.cursor/` (Cursor's Bugbot would apply these
  rules to an author's dissertation).

## P1 - the thesis build

- `build-thesis.yml` builds from committed files and never fetches the registry
  or any class at build time. Flag any download of a `.cls`, a profile or a
  partial in CI. (Installing the pinned TeX Live snapshot is not a class download.)
- TeX Live is pinned: `TL_SNAPSHOT`, `TL_INSTALLER_SHA512` and `TL_TLPDB_SHA512`
  in the Install TeX Live step of `build-thesis.yml` and
  `template-thesis-check.yml` equal `tools/texlive-pin.txt` in the registry at
  the commit in `registry-source.json` (checked by `template-thesis-check.yml`).
  The installer is downloaded to a file and checked before it is unpacked, and
  `install-tl` and `tlmgr` use only the snapshot. Flag a pin changed in one file
  only, an install from the current CTAN mirror, and an unchecked download.
- Quarto and the LaTeX engine agree: `documentclass: dataimago-thesis`,
  `pdf-engine: lualatex`, the six `template-partials` and the `thesis-divs.lua`
  filter in `_quarto.yml` match the files in `ui/www/thesis-class/`;
  `ui/www/_environment` puts `thesis-class/` and `profiles/` on `TEXINPUTS`;
  `thesis.profile` names a profile that has both `.yaml` and compiled `.cfg` in
  `ui/www/profiles/`; the `output-file: thesis` name matches `docs/thesis.pdf`.
  The workflow installs the pinned TeX Live with the TeX Gyre fonts (the package
  list of the registry's `tools/texlive-packages.txt`) and checks the fonts the
  PDF embeds (`check-pdf-fonts.sh`): a silent math-font fallback to Latin
  Modern Math must fail the run.
- `.gitignore` ignores `*.tex`; the vendored partials (`thesis-class/*.tex`)
  must stay un-ignored.
- The vendored class is byte-identical to the registry at the commit in
  `ui/www/thesis-class/registry-source.json` (`sync.py check`, run by
  `template-thesis-check.yml`). Flag a hand edit of a vendored file, and a change
  to `registry-source.json` that is not the output of `sync.py sync`.
- `template-thesis-check.yml` is template-only: every job keeps the
  `github.repository == 'dataimago/dissertation-rpkg-template'` guard. The sample
  thesis must render to a tagged PDF with the profile's fonts.
- The `{{` guard in `build-thesis.yml` and the `!=` template guards on the
  other workflows stay, so a raw template copy does not fail CI.

## P1 - the registry contract

- Docs and agent guidance about the three `classFile` modes (`shipped`,
  `vendored`, `generated`) must match `dataimago/dissertation-thesis-classes`
  (`registry.json` at `schemaVersion` 2, `docs/discovery-contract.md`,
  `docs/house-class-spec.md`): an institution is found in `profiles`
  (`mode: shipped`, `status: available`), the profile's `class` is resolved in
  `classes`, and the class `path` + `companions` (under `classes/<class>/`) and
  the profile's `cfg` + `yaml` (under `profiles/`) are fetched. `shipped` always
  names an institution's profile, never the `house` profile; `generated` starts
  from the `house` profile; `vendored` is the author's own class.
- `AGENTS.md`, `THESIS-CLS-README.md` and `_quarto.yml` comments must tell the
  same story about which mode does what, and about where a profile lives
  (`ui/www/profiles/<id>.yaml` + `.cfg`).

## P2 - R package hygiene

- `R CMD check` passes: `DESCRIPTION` fields, `NAMESPACE` (generated, not
  hand-edited), `.Rbuildignore`, and `Depends`/`Imports`/`Suggests` agree with
  the code. New functions have roxygen docs and a testthat test that runs.
- No hand-edited version bump in `DESCRIPTION`; `NEWS.md` updated for
  user-visible changes.
- Do not hand-edit synced design files (`ui/www/assets/neutral-*.scss`,
  `ui/www/assets/fonts/`); site rules go in `ui/www/assets/site.scss`.

## P2 - docs

- `AGENTS.md`, `README.md` and `ui/www/THESIS-CLS-README.md` agree with the
  files that exist (paths, workflow names, class options).
- Write for a dissertation author who may be new to GitHub: explain a term on
  first use, give the exact click path or command, avoid maintainer jargon.

## Alignment concern format

When a changed line conflicts with the author-agency commitments (the author's
scholarship stays theirs; AI proposes, the author decides; public-by-default
repos warn before unpublished work), title the finding
`Alignment concern: <short slug>` with `Location:`, `Contract/evidence:`,
`Impact:` and `Corrective action:` lines. PR-level feedback only; never a score
or release decision.

## Boundaries

- Review the PR diff. Read unchanged code only when needed to verify a contract
  a changed line relies on. Never read `.env*`, keys, `node_modules/`, build
  output, or unpublished manuscript content.
- The hub (`dissertation-ai`), the app template and the registry
  (`dissertation-thesis-classes`) are other repos: point to them, do not flag
  their code.
- Do not approve, merge, publish or deploy. Do not treat generated output as
  authority over its canonical source.

This file sets review instructions only. It is read by
`.github/workflows/composer-review.yml`, and exists in the template alone.
