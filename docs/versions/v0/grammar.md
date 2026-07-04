<!--
SPDX-License-Identifier: Apache-2.0
-->

# Korml v0 Grammar

This page defines the v0 grammar at the token level.
v0 is the unversioned, YAML-compatible, single-document language.
The node grammar is the same as v1; the stream/document-boundary wrapper is not present.

!!! note "Status"
    Korml v0 is intended as the YAML-compatible minimal source format: one document, no version header, and no support for multiple documents.

## Notation

| Form | Meaning |
| --- | --- |
| `A ::= B` | `A` is defined as `B`. |
| `A?` | zero or one occurrence of `A`. |
| `A*` | zero or more occurrences of `A`. |
| `A+` | one or more occurrences of `A`. |
| `A \| B` | either `A` or `B`. |
| `TOKEN` | a lexer token. |
| `ε` | an empty production. |

Whitespace, comments, and blank lines are trivia from the point of view of the semantic document model.
They are nevertheless retained by the concrete syntax tree.

## Token classes

The v0 parser is defined over these token classes:

```ebnf
WHITESPACE
COMMENT
NEWLINE
EOF

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

v0 does not use `VERSION_DIRECTIVE`, `DOC_START`, or `DOC_END` tokens.
A source containing a version directive or document boundary marker is not a valid v0 source.

## Source

A v0 source text represents exactly one implicit document.
The document may be empty.

```ebnf
Source ::= Trivia* Node? Trivia* EOF
```

There is no version directive and no explicit document start marker.
The version is implicit: a source parsed as v0 is a Korml v0 document.

Examples of complete v0 sources:

```korml
name: example
enabled: true
```

```korml
- alpha
- beta
- gamma
```

## Nodes

```ebnf
Node ::= BlockNode
       | FlowNode
       | Scalar
       | Empty

BlockNode ::= BlockMapping
            | BlockSequence

FlowNode ::= FlowMapping
           | FlowSequence

Empty ::= ε
```

A node is the syntactic form that represents a document-model value.
The document model has only mappings, sequences, scalars, and the empty document.

## Block mappings

```ebnf
BlockMapping ::= MappingEntry+

MappingEntry ::= SimpleKey COLON MappingValue?

SimpleKey ::= Scalar

MappingValue ::= InlineValue
               | NestedBlockValue
               | Empty

InlineValue ::= Trivia* (FlowNode | Scalar)

NestedBlockValue ::= Trivia* NEWLINE INDENT BlockNode DEDENT
```

Only simple scalar keys are part of Korml v0.
Complex keys are intentionally excluded.

Example:

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

SequenceEntry ::= DASH_ITEM SequenceValue?

SequenceValue ::= InlineValue
                | NestedBlockValue
                | Empty
```

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
            | Empty

FlowScalar ::= SQ_SCALAR
             | DQ_SCALAR
             | PLAIN_SCALAR
```

Block scalars are block constructs and are not flow scalar forms.

## Scalars

```ebnf
Scalar ::= SQ_SCALAR
         | DQ_SCALAR
         | PLAIN_SCALAR
         | LITERAL_BLOCK_SCALAR
         | FOLDED_BLOCK_SCALAR
```

At the language level, scalar values are text.
Boolean, integer, floating-point, date, and application-specific interpretation belong to a schema or decoding layer, not to the core grammar.

## Trivia

```ebnf
Trivia ::= WHITESPACE
         | COMMENT
         | NEWLINE
```

Trivia does not create document-model values.
It is part of the concrete syntax and must be retained by round-trip preserving implementations.
