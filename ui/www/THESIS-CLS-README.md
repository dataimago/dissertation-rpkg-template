# The thesis class and your institution's profile

Your dissertation's PDF is formatted by one LaTeX class, the **house class** `dataimago-thesis`, plus a small **profile** that holds your institution's formatting rules: margins, type size, spacing, the order of the front pages, page numbers, and so on. A profile is a list of facts about your institution's guide. You do not write a class; you fill in or choose a profile.

The house class and the profiles come from the [thesis-class registry](https://github.com/dataimago/dissertation-thesis-classes), a shared collection that this folder holds a copy of.

## What is in this folder

| Path | What it is | Edit it? |
|---|---|---|
| `thesis-class/` | The house class (`dataimago-thesis.cls`), the Quarto partials and filter that connect it to your book, and the profile generator (`thesis-profile.lua`) | **No.** Copied from the registry. |
| `thesis-class/registry-source.json` | Which registry commit the copy came from, and the files it holds | No; `sync.py` writes it. |
| `thesis-class/sync.py` | Checks the copy against the registry, and updates it | Run it; do not edit it. |
| `thesis-class/check-pdf-fonts.sh` | The build's font check (see "The build") | No. |
| `profiles/<id>.yaml` | A profile: the facts from a formatting guide, each cited to its page or section | Yes, for a profile of your own. |
| `profiles/<id>.cfg` | The profile compiled for LaTeX. The class reads only this file. | No; it is generated from the `.yaml`. |
| `_environment` | Puts `thesis-class/` and `profiles/` on LaTeX's search path when Quarto renders from this folder | No. |
| `_quarto.yml` | The book, and the `thesis:` block (your name on the title page, the degree, the committee) | Yes. |

The copy starts with one profile, `house`, the neutral default. No institution's guide stands behind it.

## Which mode are you in?

Your choice is recorded in the app repo's `dataimago-spec.yaml`, at `vertical.dissertation.thesis.classFile.type`:

- **`shipped`**: the registry has a profile for your institution, and you use it as-is. See "Setting up a shipped profile" below.
- **`vendored`**: you provide your institution's own class file. Put it in this folder, set `documentclass`, `classoption` and `pdf-engine` in `_quarto.yml` for it, and remove the `template-partials` and `filters` lines, the `thesis:` block and `_environment` if it does not use them; the house class is then not used. Your `build-thesis.yml` run then needs the LaTeX packages your class asks for.
- **`generated`** (the default): you start from the `house` profile and adapt it to your institution's formatting guidelines. See "Your own profile (generated mode)" below.

If your repository was set up before 2026-11-07, `shipped` in your spec meant the framework's old default class. Under today's meaning that is `generated`; change the spec to `generated`, unless the registry has a profile for your institution and you want to use it.

## The build

`build-thesis.yml` renders with Quarto and **LuaLaTeX**, which produces a tagged (accessible) PDF/A PDF. XeLaTeX also works, but the PDF is then untagged; set `pdf-engine: xelatex` in `_quarto.yml` only if you must. The fonts are TeX Gyre, which come with TeX Live; nothing is installed from the web but TeX Live itself. The last step of the build fails the run if the PDF embeds a different font from the profile's (LaTeX falls back to Latin Modern Math without an error when it cannot find a math font).

Locally, from this folder: `quarto render --to pdf`. You need a current TeX Live (2026 or newer, for example Homebrew's `texlive`, MacTeX, or TeX Live from `tug.org`) with the TeX Gyre fonts, `luamml`, `tagpdf` and `latex-lab`; the full distributions have them.

`build-thesis.yml` builds from the files in this folder and never downloads a class. The copy only changes when you change it.

## What you write, and where

- **The title page and front matter data** are the `thesis:` block in `_quarto.yml`: `profile`, `institution`, `degree`, `department`, `advisors`, `committee` and optionally `graduate-school`, `keywords`, `year`, `type`, `previous-degrees`, `irb-protocol`. The starter has a stand-in for each field the class requires (`Your Department`, `Your Advisor`); replace them. The class stops the build, naming the key, if one is empty.
- **Title, subtitle, author, date** are the usual `book:` keys.
- **The abstract** is the `abstract:` field in `index.qmd`. **Acknowledgments, dedication, preface, abbreviations and symbols** are divs (`::: {.acknowledgments}`) in `chapters/00-front-matter.qmd`. For the PDF, the filter lifts them into the pages the profile orders and drops that chapter; the web book shows it as written. A page you do not write is left out.
- **Formatting rules do not go in `_quarto.yml`.** Keys that the profile now owns (`geometry`, `mainfont`, `sansfont`, `mathfont`, `fontsize`, `linestretch`, `toc`, `colorlinks`, ...) are ignored with a warning in the build log that names the profile field to change instead. The starter's old `mainfont`, `sansfont`, `mathfont` and `classoption: [oneside, 12pt]` are gone for that reason: the profile sets the fonts (`type.*`) and the one-sided layout (`geometry.sides`).
- **Figures need alt text** (`fig-alt`), because the profile turns accessibility checks on.

## Setting up a shipped profile

Ask your AI assistant: *"Set up my shipped thesis profile."* It does the steps below. They are written out so you can follow what it does.

1. **Find your institution.** Read `vertical.dissertation.institution.name` in the app repo's `dataimago-spec.yaml`.
2. **Look it up in the registry.** Download `https://raw.githubusercontent.com/dataimago/dissertation-thesis-classes/main/registry.json`. Check that `schemaVersion` is `2`. In its `profiles` list, find the entry whose `institution` matches your institution's name (ignoring capital letters and extra spaces), with `mode: shipped` and `status: available`. If a name is close but not the same (for example "CU Boulder" for "University of Colorado Boulder"), ask the author to confirm before going on. Never use the profile named `house` as a shipped profile.
3. **Fetch the profile.** From this folder, run `python3 thesis-class/sync.py sync --ref main --profile <id>` (`<id>` is the profile's `id` in the registry, such as `cu-boulder`, not the institution's name). It copies the class and companions of the profile's `class` (under `classes/<class>/` in the registry), the profile's `yaml` and `cfg` (under `profiles/`), and records the commit in `thesis-class/registry-source.json`. (Without `--ref main` it works at the commit already recorded, which keeps the class as it is but only knows the profiles that existed then.)
4. **Point the book at it.** In `_quarto.yml` set `thesis.profile: <id>`. Nothing else in `format:` changes: the profile's `classOptions` is `profile=<id>`, which `thesis.profile` already sends to the class, and the engine is the class's (`lualatex`).
5. **Read what the profile does not say.** Open `profiles/<id>.yaml`. Fields the institution's guide does not state are listed under `unstated` and keep the house value; the sources are cited in `sources`. Do not tell the author that the guide is fully met without reading both lists. Fill the `thesis:` block, then render (`quarto render --to pdf`) until the PDF builds, and compare it with the guide.
6. **Commit the files** (`thesis-class/`, `profiles/`, `_quarto.yml`) on a branch and open a pull request, naming the profile and the registry commit in the message, for example "thesis: use the University of Colorado Boulder profile (registry aae193c)". To update the class later, repeat step 3 and read the pull request's diff.

**If the registry has no profile for your institution,** the assistant says so plainly, for example: "The thesis-class registry has no ready-made profile for <your institution>. It has profiles for: University of Colorado Boulder." It then offers `generated`: keep the house class and adapt the `house` profile to your institution's guidelines. If you agree, it changes `classFile.type` to `generated` in the app repo's spec. If the registry cannot be downloaded at all, the assistant tells you that too, and leaves your current setup alone rather than guessing.

## Your own profile (generated mode)

Your formatting guidelines are in your app repo at `raw/thesis-formatting/<filename>` (you attached them during the interview). If you have none yet, the `house` profile is used unchanged until you add them.

1. **Ask your AI assistant:** *"Turn my formatting guide into a profile"* (in Claude Code, `/thesis-format`). It copies `profiles/house.yaml` to `profiles/<id>.yaml` and changes only what the guide states, citing the page or section for each value and listing what the guide leaves unstated.
2. **Compile it:** from this folder, `texlua thesis-class/thesis-profile.lua profiles <id>` writes `profiles/<id>.cfg`. (Use `quarto pandoc lua` in place of `texlua` if you do not have TeX Live's.)
3. **Select it:** set `thesis.profile: <id>` in `_quarto.yml`, render, and compare the PDF with the guide. Repeat until it matches. Check every value against the guide yourself.
4. **Push.** `build-thesis.yml` rebuilds the PDF.

Do not edit `house.yaml` itself or the class; `python3 thesis-class/sync.py check` tells you when a copied file was changed. If a rule seems to need the class changed, say so to the registry's maintainers instead.

Most institutional formatting differs from the house profile in:

- **Margins** (typical: 1.5 in left for binding, 1 in elsewhere)
- **Title page wording and layout**, and which front pages exist and in what order
- **Heading style, spacing and numbering**
- **Page numbers** (position, roman front matter, first page shown or not)
- **Font and type size** (some institutions require Times New Roman or 12 pt; the house default is TeX Gyre Termes, a Times clone)
- **Citation style** (APA, Chicago, institution-specific): set with `csl:` in `_quarto.yml`, not in the profile

## Keeping the copy current

`thesis-class/registry-source.json` records the registry commit. To see whether the copy is intact: `python3 thesis-class/sync.py check` (it compares each file to the registry at that commit). To move to a newer registry version: `python3 thesis-class/sync.py sync --ref main`, then read `git diff`, render, and commit the result as a pull request.

## If your repository was set up with the older `thesis.cls`

Repositories created before the house class carry `ui/www/thesis.cls`, `ui/www/dataimago.sty`, `documentclass: thesis`, `pdf-engine: xelatex` and a `build-thesis.yml` that installs Noto fonts. They keep building as they were. To move to the house class, ask your AI assistant to copy `thesis-class/`, `profiles/` and `_environment` from the [template](https://github.com/dataimago/dissertation-rpkg-template/tree/main/ui/www), add the `thesis:` block and `format: pdf:` settings from the template's `_quarto.yml`, move the abstract, acknowledgments and dedication into the places named above, replace `build-thesis.yml` with the template's, and delete `thesis.cls` and `dataimago.sty`. Your formatting rules then move to a profile.
