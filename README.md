# {{rPackage.name}}

> R package supporting {{user.name}}'s dissertation, "{{thesis.workingTitle}}", provisioned via [dissertation.ai](https://dissertation-ai.dataimago.ai).

**📖 Website:** [{{user.githubUsername}}.github.io/{{rPackage.name}}](https://{{user.githubUsername}}.github.io/{{rPackage.name}}/) — the thesis as an HTML book, the latest thesis PDF, and the R package reference rendered from the roxygen docs. Published by `quarto-publish.yml` on every push (a maintainer or the provisioning flow must enable GitHub Pages, build type "GitHub Actions", once).

This package is the **R-package half** of a two-repo dissertation environment. The NextJS app half lives at [`github.com/{{user.githubUsername}}/{{metadata.name}}`](https://github.com/{{user.githubUsername}}/{{metadata.name}}) and includes this package as a Git submodule at `packages/r-packages/{{rPackage.name}}/`.

## What's in this repo

| Path | Purpose |
|---|---|
| `R/` | Your methodological R code |
| `tests/testthat/` | Unit tests |
| `ui/www/` | The Quarto book that becomes your thesis PDF |
| `ui/www/chapters/` | Per-chapter `.qmd` sources |
| `ui/www/thesis.cls` | LaTeX thesis class (see `ui/www/THESIS-CLS-README.md` for the 3-mode strategy) |
| `ui/www/references.bib` | BibTeX bibliography |
| `.github/workflows/build-thesis.yml` | Renders thesis PDF on every push that touches `ui/www/` or `R/` |
| `.github/workflows/quarto-publish.yml` | Publishes the HTML book + PDF + package reference to GitHub Pages |
| `.github/workflows/R-CMD-check.yml` | R package CI |
| `.github/workflows/design-sync-check.yml` | Fails if the web book's synced theme or fonts were edited by hand (see "The site's look") |
| `DESCRIPTION` | R package metadata |

## Quick start

```sh
git clone https://github.com/{{user.githubUsername}}/{{rPackage.name}}.git
cd {{rPackage.name}}

# Edit chapter content in ui/www/chapters/*.qmd
# (or open this repo in your AI-enabled editor)

# Local thesis PDF preview
cd ui/www && quarto preview

# Or push to main + check the CI-built PDF in docs/thesis.pdf
```

## Editing your dissertation

| What you want to change | Where |
|---|---|
| Thesis chapter content | `ui/www/chapters/*.qmd` |
| Bibliography | `ui/www/references.bib` |
| Thesis formatting (margins, title page, etc.) | `ui/www/thesis.cls` (see `ui/www/THESIS-CLS-README.md`) |
| Quarto book config (chapters list, PDF format, fonts) | `ui/www/_quarto.yml` |
| Methodology R code | `R/*.R` |

## The site's look

The published web book (not the PDF, which follows your thesis class) takes
its theme and fonts from the dataimago neutral design system,
`@dataimago/css-neutral`: Noto Sans throughout, a light and a dark theme,
contrast that meets WCAG AA. They are copies, made by `dataimago-sync` at the
version `ui/www/.dataimago/design.json` pins: `ui/www/assets/neutral-light.scss`,
`ui/www/assets/neutral-dark.scss` and `ui/www/assets/fonts/`. Each copied text
file starts with a "do not edit" line naming that version. The fonts are served
from your site, not from Google.

- **Never edit the copies.** The `Design sync check` workflow fails if one
  changes. A rule of your own goes in `ui/www/assets/site.scss`, the site's own
  layer over the theme.
- **To upgrade**, change `version` in `ui/www/.dataimago/design.json` to a newer
  release, then from `ui/www/` run
  `npx -p @dataimago/css-neutral@<version> dataimago-sync` and commit what it
  writes. Render with `quarto render --to html --profile web` and look before
  you push: a release can change how pages look.
- **To go your own way**, delete `ui/www/.dataimago/design.json`. The check then
  skips, the files are yours to edit, and nothing else depends on them.

## The two-repo relationship

This R package + the dissertation app at `github.com/{{user.githubUsername}}/{{metadata.name}}` are designed to be edited together. Most users clone the app repo with `--recursive` to get both at once. Changes to thesis content + R code go in this repo; changes to the spec + landing page + app-level configuration go in the app repo.

## Framework links

- [dissertation.ai](https://dissertation-ai.dataimago.ai) — the hub that provisioned this repo
- [dataimago](https://github.com/dataimago/dataimago) — the framework this package is built on
- [dissertation-rpkg-template](https://github.com/dataimago/dissertation-rpkg-template) — the template this repo was made from

## License

MIT
