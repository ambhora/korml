<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml Language Specification

Korml is a small markup language for structured configuration-like documents.
This site documents the language itself, not a particular implementation API.

The specification is organized by language version.

| Version | Source shape | YAML relationship | Intended use |
| --- | --- | --- | --- |
| [v0](versions/v0/index.md) | one implicit document, no version directive, no document stream | YAML-compatible single-document subset | simple single-file configuration |
| [v1](versions/v1/index.md) | version directive plus one or more explicit documents | Korml stream; document bodies use the v0 body grammar | versioned streams and multi-document sources |

The important compatibility point is version-specific: **v0 is the YAML-compatible form**.
v0 corresponds to the JSON-shaped single-document subset of YAML.

v1 reuses the same document-body grammar, but a complete v1 source is not intended to be a plain YAML document because it has a Korml version directive and explicit stream boundaries.
