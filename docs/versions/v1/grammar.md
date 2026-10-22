<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml v1 Grammar

This page defines the v1 grammar at the token level.
The grammar is intentionally written over lexer tokens rather than directly over characters.
This keeps the parser specification independent of the exact scanner implementation while still supporting a full-fidelity concrete syntax tree.

!!! note "Status"
    Korml v1 is the versioned stream format. It keeps the v0 document body grammar and adds a required Korml version directive plus explicit document boundaries. The complete v1 source is a Korml stream rather than the YAML-compatible source form.

## Notation

| Form | Meaning |
| --- | --- |
| `A ::= B` | `A` is defined as `B`. |
| `A?` | zero or one occurrence of `A`. |
| `A*` | zero or more occurrences of `A`. |
| `A+` | one or more occurrences of `A`. |
| `A \| B` | either `A` or `B`. |
| `TOKEN` | a lexer token. |

Whitespace, comments, and blank lines are trivia from the point of view of the semantic document model.
They are nevertheless retained by the concrete syntax tree.

Unless otherwise stated, grammar examples in this reference are document-body fragments.
A complete Korml v1 source stream starts with `%!korml version 1.0`, and each of its documents is enclosed by a document start marker `---` and a document end marker `...`.

## Document body grammar

v1 document bodies use the same restricted grammar as v0.
In practice this means ordinary mapping and sequence bodies, plus JSON-like flow mappings and flow sequences, are valid inside a v1 stream when they use only scalar keys and scalar leaf values.

```korml
name: example
enabled: true
count: 3
tags: [small, portable]
limits: { ranks: 4, threads: 8 }
```

A v0-style body can be placed in the v1 stream envelope:

```korml
%!korml version 1.0
---
name: example
enabled: true
count: 3
tags: [small, portable]
limits: { ranks: 4, threads: 8 }
...
```

The YAML-compatible complete-source form is v0.
A complete v1 source has Korml-specific stream syntax, so it should not be described as a plain YAML-compatible document.

Anchors, aliases, tags, complex keys, merge keys, and implicit YAML type resolution are outside the core grammar.

## Token classes

The v1 parser is defined over these token classes:

```ebnf
WHITESPACE
COMMENT
NEWLINE
EOF

VERSION_DIRECTIVE
DOC_START
DOC_END

INDENT
DEDENT

DASH_ITEM
COLON

FLOW_SEQUENCE_START
FLOW_SEQUENCE_END
FLOW_MAPPING_START
FLOW_MAPPING_END
FLOW_SEPARATOR

SQ_SCALAR
DQ_SCALAR
PLAIN_SCALAR
LITERAL_BLOCK_SCALAR
FOLDED_BLOCK_SCALAR
```

`INDENT` and `DEDENT` are abstract layout tokens.
An implementation may either emit them explicitly or derive the same structure from retained whitespace tokens.

## Stream

A v1 source text represents a stream of one or more documents prefixed by a version directive.

```ebnf
Stream ::= VersionDirective Trivia* DocumentSequence EOF

VersionDirective ::= VERSION_DIRECTIVE

DocumentSequence ::= ExplicitDocument+
```

The version directive is stream metadata.
It is not a mapping entry, sequence item, or scalar value in the document model.
For Korml v1, the source-level version header is written as:

```korml
%!korml version 1.0
```

## Documents

```ebnf
ExplicitDocument ::= DOC_START Trivia* Node? Trivia* DOC_END Trivia*
```

A document may be empty.
An empty document has no root node.
Each v1 document starts with `DOC_START` and ends with `DOC_END`.
The end marker is required for every document, including the last one in the stream: a document that reaches the next `---` or the end of the source without its `...` is not valid.
Trivia after `DOC_END`, such as the line break that ends the `...` line or a comment between documents, belongs to the stream and has no document-model value.

`DOC_START` and `DOC_END` are syntactic document-boundary markers.
They are preserved by the concrete syntax tree.

## Nodes

```ebnf
Node ::= BlockNode
       | FlowNode
       | Scalar

BlockNode ::= BlockMapping
            | BlockSequence

FlowNode ::= FlowMapping
           | FlowSequence
```

A node is the syntactic form that represents a document-model value.
The document model has only mappings, sequences, scalars, and empty documents.
An empty document is a document with no node between its markers.
There is no empty node anywhere else: every mapping entry, sequence entry and flow entry has a value.

## Block mappings

```ebnf
BlockMapping ::= MappingEntry+

MappingEntry ::= SimpleKey COLON MappingValue

SimpleKey ::= Scalar

MappingValue ::= InlineValue
               | NestedBlockValue

InlineValue ::= Trivia* (FlowNode | Scalar)

NestedBlockValue ::= Trivia* NEWLINE INDENT BlockNode DEDENT
```

Only simple scalar keys are part of Korml v1.
Complex keys are intentionally excluded.

Every mapping entry has a value: a key followed by nothing, as in `key:`, is not valid.
An empty string is written `""`, an empty sequence `[]` and an empty mapping `{}`.

Examples:

```korml
title: Example
count: 3
nested:
  enabled: true
  target: local
```

## Block sequences

```ebnf
BlockSequence ::= SequenceEntry+

SequenceEntry ::= DASH_ITEM SequenceValue

SequenceValue ::= InlineValue
                | NestedBlockValue
```

Every sequence entry has a value: a dash followed by nothing is not valid.

Examples:

```korml
- alpha
- beta
- gamma
```

```korml
- name: first
  enabled: true
- name: second
  enabled: false
```

## Flow mappings

```ebnf
FlowMapping ::= FLOW_MAPPING_START Trivia* FlowMappingEntries? Trivia* FLOW_MAPPING_END

FlowMappingEntries ::= FlowMappingEntry (Trivia* FLOW_SEPARATOR Trivia* FlowMappingEntry)*

FlowMappingEntry ::= SimpleKey Trivia* COLON Trivia* FlowValue
```

Example:

```korml
{ name: example, enabled: true }
```

## Flow sequences

```ebnf
FlowSequence ::= FLOW_SEQUENCE_START Trivia* FlowSequenceEntries? Trivia* FLOW_SEQUENCE_END

FlowSequenceEntries ::= FlowValue (Trivia* FLOW_SEPARATOR Trivia* FlowValue)*
```

Example:

```korml
[alpha, beta, gamma]
```

## Flow values

```ebnf
FlowValue ::= FlowMapping
            | FlowSequence
            | FlowScalar

FlowScalar ::= SQ_SCALAR
             | DQ_SCALAR
             | PLAIN_SCALAR
```

Block scalars are block constructs and are not flow scalar forms.

Every flow entry has a value, so `{ key: }`, `[alpha, , gamma]` and a trailing separator as in `[alpha, beta, ]` are not valid.
The empty collections `[]` and `{}` are values and remain valid.

## Scalars

```ebnf
Scalar ::= SQ_SCALAR
         | DQ_SCALAR
         | PLAIN_SCALAR
         | LITERAL_BLOCK_SCALAR
         | FOLDED_BLOCK_SCALAR
```

Korml has no block-scalar chomping indicators: `|-`, `|+`, `>-` and `>+` are not valid.
How a block scalar's final line breaks belong to its value is fixed by the [lexical structure](lexical-structure.md#block-scalars).

At the language level, scalar values are text.
This is also how Korml keeps YAML/JSON-shaped syntax separate from application typing.
Boolean, integer, floating-point, null-like, date, and application-specific interpretation belong to a schema or decoding layer, not to the core grammar.

## Trivia

```ebnf
Trivia ::= WHITESPACE
         | COMMENT
         | NEWLINE
```

Trivia does not create document-model values.
It is part of the concrete syntax and must be retained by round-trip preserving implementations.
