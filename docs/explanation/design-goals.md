<!--
SPDX-License-Identifier: Apache-2.0
-->

# Design Goals

Korml is a reduced markup language.
It keeps the parts of YAML-style documents that are useful for simple structured configuration and removes features that make parsing, tooling, and round-tripping harder.

## Small core language

The core language should be small:

- mappings,
- sequences,
- scalars,
- comments,
- document boundaries,
- flow style for compact values,
- block scalars when long text is needed.

The language should not require anchors, aliases, tags, complex keys, or implicit scalar typing in the core grammar.

## Clear separation of concerns

Korml separates concerns into layers:

| Layer | Responsibility |
| --- | --- |
| Source text | the original bytes or text. |
| Lexer | tokenization, comments, whitespace, scalar spelling, indentation. |
| Parser | token-level structure and concrete syntax tree. |
| Concrete syntax tree | round-trip preserving representation. |
| Semantic view | mappings, sequences, scalars, and documents. |
| Schema or decoder | application-specific typing and validation. |

This keeps the language specification independent of any one Python API.

## Text first, typing later

The core language treats scalar values as text.
This avoids surprising implicit conversions in the grammar.
For example:

```korml
enabled: true
count: 3
```

In the core document model, `true` and `3` are scalar text values.
A schema or decoder may later convert them to a boolean and an integer.

## Tooling-friendly syntax

Korml should be suitable for tools that need to read, modify, and write documents without destroying formatting.
That requires preserving comments, whitespace, indentation, and source spans.

A lossy abstract syntax tree is not enough for this goal.
Korml therefore uses a round-trip preserving concrete syntax tree as the central parsed representation.
