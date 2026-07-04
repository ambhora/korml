<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml v0 Examples

v0 examples are complete source files.
They do not start with a version directive and they do not use document boundary markers.

## First document

```korml
name: example
enabled: true
count: 3
```

This represents a mapping with three scalar keys and three scalar values.
At the language level, all three values are text.
A later schema or decoder may interpret `true` as a boolean and `3` as an integer.

## Nested mappings

```korml
name: example
runtime:
  system: local
  ranks: 4
```

The value of `runtime` is a nested mapping.

## Sequences

```korml
steps:
  - prepare
  - run
  - collect
```

Each sequence item is a scalar value.

## Sequences of mappings

```korml
steps:
  - name: prepare
    command: setup
  - name: run
    command: execute
  - name: collect
    command: archive
```

This is useful for structured lists.

## Flow style

```korml
name: example
tags: [small, structured, portable]
limits: { ranks: 4, threads: 8 }
```

Flow style is useful for compact values.
Block style is usually better for larger documents.

## Comments

```korml
# This is a Korml v0 document.
name: example  # This is a trailing comment.
```

Comments are not part of the document model, but they are preserved by the concrete syntax tree.

## Block scalars

```korml
description: |
  This is a longer description.
  Its source spelling should be preserved.
```

A block scalar is still a scalar value in the document model.

## Invalid v0 stream syntax

v0 has no stream wrapper, so this is not v0:

```korml
%!korml version 1.0
---
name: example
...
```

Use [v1](../v1/index.md) for versioned streams and multiple documents.
