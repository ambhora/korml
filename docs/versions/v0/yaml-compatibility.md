<!--
SPDX-License-Identifier: Apache-2.0
-->

# YAML Compatibility

Korml v0 is intended to be backward-compatible with the JSON-shaped, single-document subset of YAML.
That subset consists of the structured forms that are also familiar from JSON:

- mappings with scalar keys,
- sequences,
- nested mappings and sequences,
- quoted or plain scalar leaf values,
- flow mappings and flow sequences.

A small YAML configuration using only those forms should therefore also be a valid Korml v0 source.

```korml
name: example
enabled: true
count: 3
tags: [small, portable]
limits: { ranks: 4, threads: 8 }
```

The example above is a complete v0 source.
It has no Korml version directive and no document boundary markers, which is what makes v0 the YAML-compatible source form.

## JSON-style flow values

The flow form can be written in a JSON-like style:

```korml
{"name": "example", "enabled": true, "count": 3, "tags": ["small", "portable"]}
```

Korml still treats scalar values as text at the language level.
A schema or decoder may later interpret `true` as a boolean, `3` as an integer, or `null` as a null-like value.
Those interpretations are not part of the core grammar.

## Deliberately excluded YAML features

Korml v0 does not try to be all of YAML.
The compatible subset intentionally excludes features that make parsing, editing, and round-tripping harder:

- anchors and aliases,
- tags and application-specific YAML type resolution,
- complex mapping keys,
- merge keys,
- arbitrary implicit scalar typing,
- YAML directives,
- document-start and document-end markers,
- multiple documents in one source text.

The goal is not to replace a general YAML parser.
The goal is to keep the simple, widely used YAML/JSON-shaped configuration subset as a small Korml source format.

## Compatibility rule

A useful rule of thumb is:

> A complete Korml v0 source should be readable as the restricted, JSON-shaped, single-document subset of YAML.

For a versioned or multi-document Korml source, use [v1](../v1/index.md).
A complete v1 source is a Korml stream, not the YAML-compatible source form.
