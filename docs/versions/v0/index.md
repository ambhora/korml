<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml v0

Korml v0 is the YAML-compatible single-document form of the language.
It has no source-level version directive and no document stream syntax.

A complete v0 source can be as small as:

```korml
name: example
enabled: true
```

This is also intended to be valid in the corresponding restricted YAML subset.
The restriction is deliberate: v0 keeps the JSON-shaped parts of YAML that are useful for configuration and avoids YAML features that make parsing and round-tripping harder.

v0 supports:

- block mappings,
- block sequences,
- scalar values,
- flow mappings and sequences,
- comments,
- literal and folded block scalars,
- round-trip preserving trivia.

v0 has exactly one implicit document.
It does not support `%!korml version 1.0`, `---`, `...`, or multiple documents.
Those stream-level constructs belong to [v1](../v1/index.md).

## Pages

- [Grammar](grammar.md)
- [YAML Compatibility](yaml-compatibility.md)
- [Lexical Structure](lexical-structure.md)
- [Document Model](document-model.md)
- [Examples](examples.md)
