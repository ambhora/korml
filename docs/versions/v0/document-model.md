<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml v0 Document Model

The Korml v0 document model is the abstract data model represented by a single source text.
It is smaller than the concrete syntax tree.
It does not contain comments, whitespace, indentation, or exact source spelling.

## A complete example

A v0 source text is one implicit document.
The document has an optional root value, and that value is usually a mapping for structured configuration-like data.

```korml
name: example
runtime:
  system: local
  resources:
    ranks: 4
    threads: 8
steps:
  - name: prepare
    command: setup
  - name: run
    command: execute
tags: [tutorial, document-model]
description: |
  This is a complete Korml v0 document.
  Comments, spacing, and scalar spelling belong to the CST.
```

At the document-model level, the same source has this shape:

```text
Document
└── root: Mapping
    ├── name: Scalar("example")
    ├── runtime: Mapping
    │   ├── system: Scalar("local")
    │   └── resources: Mapping
    │       ├── ranks: Scalar("4")
    │       └── threads: Scalar("8")
    ├── steps: Sequence
    │   ├── Mapping
    │   │   ├── name: Scalar("prepare")
    │   │   └── command: Scalar("setup")
    │   └── Mapping
    │       ├── name: Scalar("run")
    │       └── command: Scalar("execute")
    ├── tags: Sequence
    │   ├── Scalar("tutorial")
    │   └── Scalar("document-model")
    └── description: Scalar("This is a complete Korml v0 document...\n")
```

This example shows the main distinction used throughout the specification: the document model contains values, while the concrete syntax tree contains the source details needed to reproduce the text.

## Document

A v0 source contains exactly one implicit document.
The document contains zero or one root value.
An empty source or a trivia-only source is an empty document.

```text
Document
└── root: Value | empty
```

## Values

Korml has three value kinds:

```text
Value ::= Mapping | Sequence | Scalar
```

### Mapping

A mapping is an ordered collection of scalar keys and values.

```korml
name: example
target: local
```

Korml v0 uses simple scalar keys.
Complex keys are not part of the core language.

### Sequence

A sequence is an ordered collection of values.

```korml
- alpha
- beta
- gamma
```

### Scalar

A scalar is a text value.

```korml
name: example
```

The core language does not assign built-in numeric, boolean, date, or null types to scalars.
Those interpretations belong to schemas, decoders, or application code.

## Concrete syntax tree and document model

The document model is not enough for exact source preservation.
A round-trip preserving implementation needs a concrete syntax tree that retains:

- comments,
- whitespace,
- blank lines,
- indentation,
- scalar source spelling,
- token spans.

v0 does not need to retain a version directive or document-boundary markers because those constructs are not part of v0 syntax.
The document model is therefore a semantic view over the concrete syntax tree, not a replacement for it.
