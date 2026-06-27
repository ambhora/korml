<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml Language Specification Site

This is a standalone MkDocs site for the Korml language specification.
It intentionally excludes Python API documentation and implementation reference material.

## Build locally

```bash
uv run -- mkdocs serve
```

or:

```bash
uv run -- mkdocs build
```

The site structure follows the four documentation axes:

- Reference
- Tutorial
- How-to
- Explanation

The home page and how-to page are currently intentionally empty.

## Code highlighting

Markdown fences marked as `korml` are configured to use YAML-based highlighting.

```markdown
```korml
%!korml version 1.0
---
name: example
...
```
```
