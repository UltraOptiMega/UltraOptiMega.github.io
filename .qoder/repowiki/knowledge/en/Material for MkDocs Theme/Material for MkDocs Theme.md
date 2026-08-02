---
kind: external_dependency
name: Material for MkDocs Theme
slug: material-for-mkdocs
category: external_dependency
category_hints:
    - vendor_identity
    - framework_behavior
scope:
    - '**'
source_files:
    - mkdocs.yml
---

### Material for MkDocs
- The documentation site uses the **Material for MkDocs** theme (declared as `theme.name: material` in mkdocs.yml).
- Configured with an Indigo color palette, light/dark mode toggle (`scheme: default` / `scheme: slate`), and features including instant navigation, search suggestions/highlighting, and code copy.
- Markdown extensions enabled via pymdownx (highlight with line-number anchors, superfences, tabbed, admonition, details) plus attr_list and md_in_html.
- This is a third-party MkDocs theme; verify exact feature flags against the official Material for MkDocs docs.