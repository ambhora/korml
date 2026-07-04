<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml v1 Examples

v1 examples are complete source streams.
They start with a version directive and each document starts with `---`.
The document bodies use the same restricted mapping/sequence/scalar grammar as v0; the complete source is a Korml stream.

## First document

```korml
%!korml version 1.0
---
name: example
enabled: true
count: 3
...
```

This represents a stream with one document.
The document root is a mapping with three scalar keys and three scalar values.
At the language level, all three values are text.
A later schema or decoder may interpret `true` as a boolean and `3` as an integer.

## Nested mappings

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

```korml
%!korml version 1.0
---
name: example
tags: [small, structured, portable]
limits: { ranks: 4, threads: 8 }
...
```

## JSON-shaped body values

A v1 document body may use the same JSON-shaped mapping/sequence/scalar forms as v0.
The complete source is still wrapped in the Korml v1 stream envelope.

```korml
%!korml version 1.0
---
{"name": "example", "enabled": true, "count": 3, "tags": ["small", "portable"]}
...
```

The values `true` and `3` are scalar text at the language level.
A schema or decoder may later interpret them as a boolean and an integer.

Flow style is useful for compact values.
Block style is usually better for larger documents.

## Comments

```korml
%!korml version 1.0
---
# This is a Korml v1 document.
name: example  # This is a trailing comment.
...
```

Comments are not part of the document model, but they are preserved by the concrete syntax tree.

## Multiple documents

A v1 stream may contain more than one document:

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

```korml
%!korml version 1.0
---
description: |
  This is a longer description.
  Its source spelling should be preserved.
...
```

A block scalar is still a scalar value in the document model.

## Relationship to v0

The document body below is valid in both versions:

```korml
name: example
tags: [small, structured]
```

In v0, that text is the complete source.
In v1, that text must appear inside the versioned stream wrapper.
