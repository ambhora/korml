<!--
SPDX-License-Identifier: Apache-2.0
-->

# Grammar Reference

This page defines the Korml grammar at the token level.
The grammar is intentionally written over lexer tokens rather than directly over characters.
This keeps the parser specification independent of the exact scanner implementation while still supporting a full-fidelity concrete syntax tree.

!!! note "Status"
    This is a language-specification draft for Korml v1. It captures the current intended shape of the language: mappings, sequences, scalars, comments, document boundaries, flow forms, and round-trip preserving trivia.

## Notation

The grammar uses the following notation:

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

Unless otherwise stated, grammar examples in this reference are document-body fragments. A complete Korml source stream starts with `%!korml version 1.0` and an explicit document start marker `---`.

## Token classes

The parser is defined over these token classes:

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

A Korml source text represents a stream of one or more documents prefixed by a version directive.

```ebnf
Stream ::= VersionDirective Trivia* DocumentSequence EOF

VersionDirective ::= VERSION_DIRECTIVE

DocumentSequence ::= Document+
```

The version directive is stream metadata.
It is not a mapping entry, sequence item, or scalar value in the document model.
For Korml v1, the source-level version header is written as:

```korml
%!korml version 1.0
```

## Document

```ebnf
Document ::= Trivia* ExplicitDocument Trivia*

ExplicitDocument ::= DOC_START Trivia* Node? Trivia* DOC_END?
```

A document may be empty.
An empty document has no root node. A valid source stream starts with a version directive and an explicit document start marker.

`DOC_START` and `DOC_END` are syntactic document-boundary markers.
They are preserved by the concrete syntax tree.

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
The document model has only mappings, sequences, scalars, and empty documents.

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

Only simple scalar keys are part of Korml v1.
Complex keys are intentionally excluded.

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
