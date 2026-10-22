<!--
SPDX-License-Identifier: Apache-2.0
-->

# Language Versions

Korml versions are documented separately because the valid source envelope changes between versions.
The document body language is shared, but the top-level source form is not.

## Version summary

| Version | Version directive | Multiple documents | Document start `---` and end `...` | YAML-compatible as a complete source? | Root value |
| --- | --- | --- | --- | --- | --- |
| [v0](v0/index.md) | not supported | not supported | not supported | yes, for the restricted single-document subset | optional single root node |
| [v1](v1/index.md) | required | supported | both required for each document | no; the source is a Korml stream | optional root node per document |

## Relationship between v0 and v1

v0 is the unversioned, YAML-compatible, single-document language.
A v0 source text is a single document body:

```korml
name: example
runtime:
  ranks: 4
```

The same text is also intended to be readable as the corresponding restricted YAML subset.
That compatibility is possible because v0 does not require a version directive or multi-document stream wrapper.

v1 keeps the same document body grammar, but places each body inside a Korml stream:

```korml
%!korml version 1.0
---
name: example
runtime:
  ranks: 4
...
```

The practical rule is:

- choose v0 when the file is exactly one document and should also be acceptable as the restricted YAML/JSON-shaped subset;
- choose v1 when the file needs an explicit Korml version header, more than one document, or stream-level syntax.

## Version detection

A parser may choose the version from caller configuration.
If it performs source-based detection, the recommended rule is:

- a source beginning with `%!korml version 1.0` is v1;
- a source without a version directive is v0;
- a source containing v1 document stream markers without the v1 version directive is invalid as v0.
