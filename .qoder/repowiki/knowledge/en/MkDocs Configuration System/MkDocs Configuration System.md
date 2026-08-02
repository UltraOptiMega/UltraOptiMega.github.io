---
kind: configuration_system
name: MkDocs Configuration System
category: configuration_system
scope:
    - '**'
source_files:
    - mkdocs.yml
    - docs/index.md
---

This repository uses MkDocs as its static documentation site generator, with all configuration centralized in a single `mkdocs.yml` file at the repository root. There is no custom configuration loading logic — MkDocs natively reads this YAML file to configure the site.

**What system/approach is used:**
- MkDocs YAML-based configuration (`mkdocs.yml`) for site metadata, theme settings, and Markdown extensions
- Material theme (v8+) configured via nested YAML properties including color palettes, dark/light mode toggles, and feature flags
- No environment variables, `.env` files, or programmatic config loaders are present

**Key files and packages:**
- `mkdocs.yml` — primary configuration file defining site name, theme, palette, features, and markdown extensions
- `docs/index.md` — single landing page content file

**Architecture and conventions:**
- Flat configuration: All site settings live in one YAML file; no splitting across multiple config files
- Theme configuration follows Material theme's schema: palette defines default/slate schemes with indigo accent colors and brightness toggle icons
- Markdown extensions use `pymdownx.*` suite plus `admonition`, `attr_list`, and `md_in_html` for enhanced rendering
- Features enabled include instant navigation, search suggestions/highlighting, code copy buttons, and section expansion
- No build-time or runtime configuration layering — the same `mkdocs.yml` is used for both development (`mkdocs serve`) and production builds

**Rules developers should follow:**
- Keep all site configuration in `mkdocs.yml`; do not split into separate config files
- Use Material theme's built-in palette and features rather than custom CSS overrides when possible
- Add new Markdown extensions under `markdown_extensions` following the existing `pymdownx.*` pattern
- Content goes under `docs/` with `index.md` as the homepage
- No secrets or environment-specific configuration is needed — this is a pure static site with no server-side logic