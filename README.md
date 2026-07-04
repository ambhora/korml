<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml Language Specification Site

This is a standalone MkDocs site for the Korml language specification.
It intentionally excludes Python API documentation and implementation reference material.

The specification is organized by language version:

- `docs/versions/v0/`: YAML-compatible, unversioned, single-document Korml.
- `docs/versions/v1/`: versioned multi-document Korml stream.

v0 and v1 share the same document body grammar.
v0 is the YAML-compatible complete source form: one implicit document, no version directive, and no document stream.
v1 adds the Korml stream wrapper: `%!korml version 1.0`, explicit document starts, optional document ends, and multiple documents.

## Build locally

```bash
uv run -- mkdocs serve
```

or:

```bash
uv run -- mkdocs build
```

## Site structure

- `docs/index.md`: site landing page.
- `docs/versions/index.md`: version overview and selection rules.
- `docs/versions/v0/`: v0 reference and examples.
- `docs/versions/v1/`: v1 reference, stream format note, and examples.
- `docs/how-to/`: task-oriented notes.
- `docs/explanation/`: design explanation that applies across versions.

## Code highlighting

Markdown fences marked as `korml` are configured to use YAML-based highlighting.

````markdown
```korml
name: example
```
````

````markdown
```korml
%!korml version 1.0
---
name: example
...
```
````
