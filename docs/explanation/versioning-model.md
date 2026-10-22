<!--
SPDX-License-Identifier: Apache-2.0
-->

# Versioning Model

Korml separates the document body language from the source envelope.
This makes it possible to keep a small YAML-compatible source form while adding a separate versioned stream form.

## v0: YAML-compatible single implicit document

v0 is the smallest complete source format.
It has no version directive and no explicit document boundaries.
The whole source text is one implicit document.

```korml
name: example
runtime:
  ranks: 4
```

This is the YAML-compatible version of Korml.
More precisely, v0 corresponds to the restricted, JSON-shaped, single-document subset of YAML.

The lack of a required version header is part of that compatibility story: a normal single-document YAML-style configuration file can also be parsed as v0 when it stays inside the supported subset.

## v1: versioned document stream

v1 adds a Korml stream wrapper.
A complete v1 source starts with a version directive, and each document is enclosed by explicit `---` and `...` boundaries.

```korml
%!korml version 1.0
---
name: example
...
```

The stream wrapper gives the parser source-level version metadata and makes multiple documents possible.
A complete v1 source should therefore be treated as a Korml stream, not as the YAML-compatible source form.

## Shared document body grammar

The body of a v0 document and the body of a v1 document use the same grammar.
This keeps the upgrade path simple:

```korml
name: example
```

can become:

```korml
%!korml version 1.0
---
name: example
...
```

without changing the document value.

The compatibility boundary remains important:

- v0 is the YAML-compatible complete source form;
- v1 reuses the v0 body grammar inside a Korml-specific stream envelope.

## Why v0 has no version header

A version header is useful when the source is a stream that may contain multiple documents or future stream-level features.
For v0, the source has exactly one implicit document.
There is no stream structure to describe, and a source-level version header would break the intended YAML-compatible single-document shape.

The implementation may still represent a parsed v0 file internally as a stream with one document, but that is an implementation convenience rather than v0 source syntax.
