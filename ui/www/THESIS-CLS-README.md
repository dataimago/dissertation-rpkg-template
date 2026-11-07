# Thesis class file (`thesis.cls`)

Your dissertation's `thesis.cls` controls how the thesis PDF is formatted: margins, title page, signature page, chapter headings, front-matter order.

## Which mode are you in?

Your choice is recorded in the app repo's `dataimago-spec.yaml`, at `vertical.dissertation.thesis.classFile.type`. The three modes come from the [thesis-class registry](https://github.com/dataimago/dissertation-thesis-classes), a shared collection of ready-made classes for particular institutions:

- **`shipped`**: the registry has a class for your institution, and you use it as-is. See "Setting up a shipped class" below.
- **`vendored`**: you provide your institution's own class file. Replace this `thesis.cls` with your institution's file, commit, and push; the next `build-thesis.yml` run uses it.
- **`generated`**: you start from the framework's default `thesis.cls` (the file in this folder now) and tailor it to your institution's formatting guidelines. See "Tailoring the default (generated mode)" below. This is the usual choice.

The `thesis.cls` in this folder is the framework's generic default. It is where `generated` starts. It is not what `shipped` means: a shipped class comes from the registry and replaces this file.

If your repository was set up before 2026-11-07, `shipped` in your spec meant this framework default. Under today's meaning that is `generated`. Change the spec to `generated`, unless the registry has a class for your institution and you want to use it.

## Setting up a shipped class

Ask your AI assistant: *"Set up my shipped thesis class."* It does the steps below. They are written out so you can follow what it does.

1. **Find your institution.** Read `vertical.dissertation.institution.name` in the app repo's `dataimago-spec.yaml`.
2. **Look it up in the registry.** Download `https://raw.githubusercontent.com/dataimago/dissertation-thesis-classes/main/registry.json`. In its `classes` list, find the entry whose `institution` matches your institution's name (ignoring capital letters and extra spaces), with `mode: shipped` and `status: available`. If a name is close but not the same (for example "CU Boulder" for "University of Colorado Boulder"), ask the author to confirm before going on.
3. **Download the class files.** From the same address, `https://raw.githubusercontent.com/dataimago/dissertation-thesis-classes/main/`, download the entry's `path` and every file in its `companions`. Save the class as `ui/www/<documentclass>.cls`. Every registry class today has `documentclass: thesis`, so it replaces the framework default `ui/www/thesis.cls`. Save each companion in `ui/www/` under its own file name.
4. **Point the Quarto config at it.** In `ui/www/_quarto.yml`, under `format:` → `pdf:`, set `documentclass:` to the entry's `documentclass`, `classoption:` to its `classOptions`, and `pdf-engine:` to its `engine`. Load each companion under `include-in-header`: `\input{<file>}` for a `.tex` file, `\usepackage{<name>}` for a `.sty` file. For the University of Colorado Boulder class, that is `documentclass: thesis`, `classoption: [defaultstyle, 11pt]`, `pdf-engine: xelatex`, and `\input{macros.tex}`.
5. **Commit the files.** Commit the class, its companions, and `_quarto.yml` on a branch and open a pull request. Name the class and its registry `version` in the commit message, for example "thesis: use the University of Colorado Boulder class (registry version 1.14)". The committed files are your copy of the class. `build-thesis.yml` builds from them and never downloads anything from the registry, so your formatting does not change unless you change it. To update the class later, repeat these steps; the pull request shows what changed.
6. **Check the PDF.** After you merge, `build-thesis.yml` rebuilds `docs/thesis.pdf`. (To see it before merging, run "Build thesis PDF" on your branch from the repository's Actions tab and download the `thesis-pdf` artifact.) Compare it with the class's example in the registry (`classes/<id>/example/`). A registry class has its own title-page commands, listed in the class's `README.md` in the registry, so the front matter may need adjusting. Make those changes in the chapters and `_quarto.yml`, not in the class: using it as-is is what `shipped` means. Two framework settings can work against a registry class: `mainfont` / `sansfont` in `_quarto.yml`, and `\usepackage{dataimago}`, which removes paragraph indents. Remove them if your institution's rules call for something else.

**If the registry has no class for your institution,** the assistant says so plainly, for example: "The thesis-class registry has no ready-made class for <your institution>. It has classes for: University of Colorado Boulder." It then offers `generated` instead: keep the framework default and tailor it to your institution's guidelines. If you agree, it changes `classFile.type` to `generated` in the app repo's spec. If the registry cannot be downloaded at all, the assistant tells you that too, and leaves your current class alone rather than guessing.

## Tailoring the default (generated mode)

Your formatting guidelines are in your app repo at `raw/thesis-formatting/<filename>` (you attached them during the interview). If you have none yet, the default is used unchanged until you add them. Recommended workflow:

1. **Open this repo in an AI-enabled editor** (Claude Code, Cursor, etc.).
2. **Ask the AI:** *"Read `raw/thesis-formatting/<filename>` in my app repo and update `ui/www/thesis.cls` to match the institutional requirements."*
3. **Push your changes.** `build-thesis.yml` rebuilds the PDF.
4. **Open the rebuilt PDF** at `docs/thesis.pdf`, compare it with the institutional sample (if any), and repeat.

Most institutional formatting differs from the framework default in:

- **Margins** (typical: 1.5in left for binding, 1in elsewhere)
- **Title page layout** (text positioning, capitalization conventions, institutional logo placement)
- **Signature page** (committee names + degree program text + signature line spacing)
- **Chapter heading style + spacing** (some institutions require specific point sizes / fonts for chapter titles)
- **Specific front-matter ordering** (Dedication → Acknowledgments → Abstract → ToC is common; some institutions require Abstract before everything)
- **Citation style** (APA / Chicago / institution-specific)
- **Specific font** (some institutions require Times New Roman; the framework default uses Noto Sans via `fontspec`)

## Switching modes

You can switch modes anytime by editing the app repo's `dataimago-spec.yaml` (`vertical.dissertation.thesis.classFile.type`) and pushing. Switching to `shipped` means following "Setting up a shipped class" above; switching back to `generated` means restoring the framework default `thesis.cls` from the [template](https://github.com/dataimago/dissertation-rpkg-template/blob/main/ui/www/thesis.cls) and its `classoption: [oneside, 12pt]`.

## What's in the framework default `thesis.cls`

The file ships with sane defaults derived from the `book` class:

- 1in margins (typical for non-binding submission)
- One-and-a-half line spacing
- Noto Sans body font (via `fontspec`; XeLaTeX-only)
- `\thesistitle{...}{...}{...}{...}{...}` — title / author / institution / degree program / year
- `\signaturepage{...}` — wraps the committee approval block
- `\sigline{...}` — single signature line helper
- `\begin{abstract}...\end{abstract}` — committee-formatted abstract environment

If your institution requires something different, the most common adjustments are 1-2 line changes (margins, font, spacing) which AI assistance can make easily.

## Adding to `dataimago.sty`

The companion `dataimago.sty` file holds LaTeX-level typography hooks. Most users won't need to edit it; institution-specific overrides are best made in `thesis.cls`.
