<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml v1 Document Model

The Korml v1 document model is the abstract data model represented by parsed source text.
It is smaller than the concrete syntax tree.
It does not contain comments, whitespace, indentation, or exact source spelling.
For the shared v0/v1 body grammar, the document-model shape is the familiar mapping/sequence/scalar tree.

## A complete example

A v1 source text is a stream.
The stream starts with a language version and then contains one or more documents.
Each document has an optional root value, and that value is usually a mapping for structured configuration-like data.

```korml
%!korml version 1.0
---
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
  This is a complete Korml v1 document.
  Comments, spacing, and scalar spelling belong to the CST.
...
```

At the document-model level, the same source has this shape:

```text
Stream
├── metadata
│   └── version: 1.0
└── documents
    └── Document
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
            └── description: Scalar("This is a complete Korml v1 document...\n")
```

This example also shows the main distinction used throughout the specification: the document model contains values, while the concrete syntax tree contains the source details needed to reproduce the text.
The same mapping/sequence/scalar model is used for v0-style body syntax and JSON-style flow syntax.

## Stream

A v1 source text represents a `Stream`.
A stream contains one or more documents and stream metadata such as the version directive.

```text
Stream
├── metadata
└── documents
```

## Document

A document contains zero or one root value.
An empty document has no root value.

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

Korml v1 uses simple scalar keys.
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
- document boundary markers,
- scalar source spelling,
- version directives,
- token spans.

The document model is therefore a semantic view over the concrete syntax tree, not a replacement for it.
