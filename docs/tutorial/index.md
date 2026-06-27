<!--
SPDX-License-Identifier: Apache-2.0
-->

# Tutorial

This tutorial introduces Korml as a small markup language for structured documents.
It focuses only on the language, not on any Python API.

## A first document

A Korml document can be a mapping:

```korml
%!korml version 1.0
---
name: example
enabled: true
count: 3
...
```

This represents a mapping with three scalar keys and three scalar values.
At the language level, all three values are text.
A later schema or decoder may interpret `true` as a boolean and `3` as an integer.

## Nested mappings

Indentation creates nested block structure:

```korml
%!korml version 1.0
---
name: example
runtime:
  system: local
  ranks: 4
...
```

The value of `runtime` is a nested mapping.

## Sequences

A sequence is written with one item per line:

```korml
%!korml version 1.0
---
steps:
  - prepare
  - run
  - collect
...
```

Each sequence item is a scalar value.

## Sequences of mappings

A sequence item may itself be a mapping:

```korml
%!korml version 1.0
---
steps:
  - name: prepare
    command: setup
  - name: run
    command: execute
  - name: collect
    command: archive
...
```

This is useful for structured lists.

## Flow style

Small mappings and sequences may be written in flow style:

```korml
%!korml version 1.0
---
name: example
tags: [small, structured, portable]
limits: { ranks: 4, threads: 8 }
...
```

Flow style is useful for compact values.
Block style is usually better for larger documents.

## Comments

Comments begin with `#` and continue to the end of the line:

```korml
%!korml version 1.0
---
# This is a Korml document.
name: example  # This is a trailing comment.
...
```

Comments are not part of the document model, but they are preserved by the concrete syntax tree.

## Multiple documents

A stream may contain more than one document:

```korml
%!korml version 1.0
---
name: first
...
---
name: second
...
```

Explicit document boundaries are useful when several documents are stored in one source text.

## Block scalars

Long text can be written as a block scalar:

```korml
%!korml version 1.0
---
description: |
  This is a longer description.
  Its source spelling should be preserved.
...
```

A block scalar is still a scalar value in the document model.

## What Korml leaves out

Korml intentionally avoids several YAML features in its core language:

- anchors and aliases,
- tags,
- complex keys,
- implicit scalar typing in the core grammar.

The goal is a smaller language with a clearer parser and a full-fidelity concrete syntax tree.
