---
kind: frontend_style
name: MkDocs Material Theme Styling
category: frontend_style
scope:
    - '**'
source_files:
    - mkdocs.yml
    - docs/index.md
---

This repository is a MkDocs documentation site that relies entirely on the built-in **Material for MkDocs** theme for all frontend styling. There are no custom CSS, SCSS, Tailwind, or component library files — visual appearance is configured exclusively through `mkdocs.yml`.

**System used:**
- The Material theme (`name: material`) provides the complete UI framework, including responsive layout, typography, code highlighting, navigation, search, and dark/light mode toggling.
- Styling customization is done via theme configuration blocks: `palette` defines color schemes (primary/accent colors per scheme), and `features` enables built-in UI behaviors like instant navigation, search suggestions, code copy buttons, and section expansion.
- Two color schemes are defined: `default` (light mode) and `slate` (dark mode), both using `indigo` as the primary and accent color with appropriate brightness icons for the mode toggle.

**Key files:**
- `mkdocs.yml` — the single source of truth for all visual and behavioral configuration. No additional style sheets or overrides exist.
- `docs/index.md` — content only; no inline styles or custom HTML affecting presentation.

**Architecture & conventions:**
- All styling decisions are declarative in the YAML config rather than imperative CSS. Developers customize appearance by editing palette entries and enabling/disabling features.
- The project follows MkDocs conventions: markdown content lives under `docs/`, and any custom assets would be placed alongside it but none are present here.
- No design tokens, CSS variables, or custom components are defined — the Material theme's defaults are used as-is except for the indigo color palette.

**Rules developers should follow:**
- Do not add custom CSS/SCSS unless absolutely necessary; prefer configuring the Material theme via `mkdocs.yml` first.
- When extending the theme, create an override directory structure (`overrides/`) following MkDocs Material's documented extension pattern rather than modifying generated output.
- Keep content separate from styling — write plain Markdown in `docs/` and rely on theme features for presentation.