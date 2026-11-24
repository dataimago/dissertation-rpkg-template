# {{rPackage.name}}

> R package supporting {{user.name}}'s dissertation, "{{thesis.workingTitle}}", provisioned via [dissertation.ai](https://dissertation-ai.dataimago.ai).

**📖 Website:** [{{user.githubUsername}}.github.io/{{rPackage.name}}](https://{{user.githubUsername}}.github.io/{{rPackage.name}}/) — the thesis as an HTML book, the latest thesis PDF, and the R package reference rendered from the roxygen docs. **This address works only once the repository is public and GitHub Pages is turned on**; while the repository is private there is no site and the link leads nowhere. See [The website](#the-website).

This package is the **R-package half** of a two-repo dissertation environment. The NextJS app half lives at [`github.com/{{user.githubUsername}}/{{metadata.name}}`](https://github.com/{{user.githubUsername}}/{{metadata.name}}) and includes this package as a Git submodule at `packages/r-packages/{{rPackage.name}}/`.

## What's in this repo

| Path | Purpose |
|---|---|
| `R/` | Your methodological R code |
| `tests/testthat/` | Unit tests |
| `ui/www/` | The Quarto book that becomes your thesis PDF |
| `ui/www/chapters/` | Per-chapter `.qmd` sources |
| `ui/www/thesis-class/` | The house LaTeX thesis class, copied from the thesis-class registry (see `ui/www/THESIS-CLS-README.md`) |
| `ui/www/profiles/` | Your institution's formatting rules as a profile (`house` to start) |
| `ui/www/references.bib` | BibTeX bibliography |
| `.github/workflows/build-thesis.yml` | Renders thesis PDF (Quarto + LuaLaTeX) on every push that touches `ui/www/` or `R/` |
| `.github/workflows/quarto-publish.yml` | Publishes the HTML book + PDF + package reference to GitHub Pages, when the repository is public (see "The website") |
| `.github/workflows/R-CMD-check.yml` | R package CI |
| `.github/workflows/design-sync-check.yml` | Fails if the web book's synced theme or fonts were edited by hand (see "The site's look") |
| `DESCRIPTION` | R package metadata |

## Quick start

```sh
git clone https://github.com/{{user.githubUsername}}/{{rPackage.name}}.git
cd {{rPackage.name}}
# (if the repository is private, git asks you to sign in to GitHub first)

# Edit chapter content in ui/www/chapters/*.qmd
# (or open this repo in your AI-enabled editor)

# Local preview of the web book (HTML)
cd ui/www && quarto preview

# Local thesis PDF: needs a current TeX Live (see ui/www/THESIS-CLS-README.md, "The build")
cd ui/www && quarto render --to pdf

# Or push to main + check the CI-built PDF in docs/thesis.pdf
```

### Building the PDF locally

You only need this to build the thesis on your own machine; pushing to `main` builds it on GitHub.

- [Quarto](https://quarto.org/docs/get-started/) at the version the build pins (`version:` in `.github/workflows/build-thesis.yml`, 1.11.9 at the time of writing; older releases are on [Quarto's download page](https://quarto.org/docs/download/prerelease.html) and its GitHub releases), so your local PDF matches the one GitHub builds.
- A current **TeX Live** (2026 or newer), for example [MacTeX](https://tug.org/mactex/) or Homebrew's `texlive` on a Mac, or TeX Live from [tug.org](https://tug.org/texlive/). TinyTeX (`quarto install tinytex`) is not enough for the house class. After installing it, run `tlmgr install tex-gyre tex-gyre-math luamml tagpdf latex-lab latexmk selnolig xurl bookmark pdflscape caption unicode-math fontspec setspace framed footnotehyper booktabs fancyvrb float xcolor colorprofiles tcolorbox fontawesome5 pgf` (from a terminal; on a system install it needs `sudo`). This is the build's own list, and a full MacTeX already has most of it.
- The fonts are TeX Gyre, which come with TeX Live. If a build complains that a font is missing, your TeX Live lacks `tex-gyre` and `tex-gyre-math`.
- R, with the packages in `DESCRIPTION`, because the chapters can run R chunks.

## Editing your dissertation

| What you want to change | Where |
|---|---|
| Thesis chapter content | `ui/www/chapters/*.qmd` |
| Bibliography | `ui/www/references.bib` |
| Thesis formatting (margins, fonts, spacing, front pages) | a profile in `ui/www/profiles/` (see `ui/www/THESIS-CLS-README.md`) |
| Title page details (degree, department, committee) | the `thesis:` block in `ui/www/_quarto.yml` |
| Quarto book config (chapters list, PDF format) | `ui/www/_quarto.yml` |
| Methodology R code | `R/*.R` |

## The website

`quarto-publish.yml` publishes the thesis as an HTML book, with the latest PDF and the R package reference, to GitHub Pages (GitHub's website hosting).

- **A private repository publishes nothing.** A GitHub Pages site is on the public web even when the repository behind it is private, so the workflow builds and deploys the site only when the repository is public. In a private repository each run ends with a notice saying nothing was published; that is not a failure.
- **To publish**, make the repository public (Settings → General → Danger Zone → Change visibility), then turn on Pages once (Settings → Pages → Source: "GitHub Actions"). The site goes live after the next push to `main`. Making the repository public shows everyone your chapters, your code and their history, not only the site.
- **To publish the site and keep the repository private**, you need a paid GitHub plan: on the free plan a private repository cannot have Pages. Turn on Pages as above, then add a repository variable named `PUBLISH_PAGES_FROM_PRIVATE` with the value `true` (Settings → Secrets and variables → Actions → Variables). Your thesis is then readable by anyone who has the address, while the repository stays private.
- **If you make a public repository private again**, on the free plan GitHub takes the site down. On a paid plan the site already published stays up until you unpublish it (Settings → Pages).
- Once the site exists, you can add its address to `URL:` in `DESCRIPTION`.

### GitHub Actions use in a private repository

A public repository runs these workflows free of charge. A private one draws on your plan's monthly GitHub Actions allowance, and on its storage for build artifacts (500 MB on the free plan at the time of writing); see [GitHub's plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) for the current figures. The first thesis build is the long one, because it installs TeX Live; later builds reuse a cached copy. The PDF kept with each run is deleted after 7 days, and the latest one is always committed to `docs/thesis.pdf`.

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

This R package + the dissertation app at `github.com/{{user.githubUsername}}/{{metadata.name}}` are designed to be edited together. Most users clone the app repo with `--recursive` to get both at once (if the repositories are private, git asks you to sign in to GitHub, and your account needs access to both). Changes to thesis content + R code go in this repo; changes to the spec + landing page + app-level configuration go in the app repo.

## Framework links

- [dissertation.ai](https://dissertation-ai.dataimago.ai) — the hub that provisioned this repo
- [dataimago](https://github.com/dataimago/dataimago) — the framework this package is built on
- [dissertation-rpkg-template](https://github.com/dataimago/dissertation-rpkg-template) — the template this repo was made from

## License

MIT
