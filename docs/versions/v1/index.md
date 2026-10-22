<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml v1

Korml v1 is the versioned stream form of the language.
It adds a Korml source envelope around one or more document bodies.

A complete v1 source starts with the version directive and a document start marker:

```korml
%!korml version 1.0
---
name: example
...
```

v1 document bodies use the same body grammar as [v0](../v0/index.md): mappings, sequences, scalars, flow collections, comments, and block scalars.
However, the compatibility boundary is different:

- a complete v0 source is the YAML-compatible single-document subset;
- a complete v1 source is a Korml stream because it requires `%!korml version 1.0` and explicit document starts and ends.

Use v1 when a source needs multiple documents, explicit Korml version metadata, or future stream-level features.

## Pages

- [Grammar](grammar.md)
- [Stream Format](stream-format.md)
- [Lexical Structure](lexical-structure.md)
- [Document Model](document-model.md)
- [Examples](examples.md)
