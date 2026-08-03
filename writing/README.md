# Writing style — three modes

`STYLE.md` in this directory is the prose register your AI assistant writes
under. Your `dataimago-spec.yaml` selects how it is sourced
(`vertical.dissertation.thesis.writingStyle`):

| Mode | What to do |
|---|---|
| `shipped` (default) | Nothing. `STYLE.md` is the dataimago technical writing spec, used as-is. |
| `vendored` | Replace `STYLE.md` wholesale with your own style guide (or point `writingStyle.path` at it). |
| `generated` | Upload exemplar prose you admire (they land in `raw/` via `context.styleExemplars`), then ask your AI assistant to distill a personal `STYLE.md` from them and approve the result before adopting it. |

As with `thesis.cls` (see the rpkg template's `THESIS-CLS-README.md`),
generated-mode work happens **in this repo, with your AI, at edit time** —
not during onboarding. The spec field can change at any point by editing
`dataimago-spec.yaml` directly.
