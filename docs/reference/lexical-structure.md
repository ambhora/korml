<!--
SPDX-License-Identifier: Apache-2.0
-->

# Lexical Structure

This page describes how Korml source text is split into tokens before parsing.
The parser consumes tokens; the concrete syntax tree keeps tokens and trivia so that source text can be emitted without losing comments, spacing, indentation, or scalar spelling.

## Characters and lines

A Korml document is a Unicode text document processed as a sequence of lines.
Line boundaries are significant for block mappings, block sequences, comments, and block scalars.

The lexer distinguishes:

- content characters,
- horizontal whitespace,
- line breaks,
- comment text,
- punctuation used by the grammar,
- scalar text.

## Whitespace

Horizontal whitespace separates tokens and contributes to indentation.
Whitespace that is not semantically significant is still retained as `WHITESPACE` trivia.

Indentation determines nesting in block style.
A Korml document should use a consistent indentation width within a document.
The language specification describes indentation through abstract `INDENT` and `DEDENT` layout tokens.

## Comments

A comment begins with `#` and continues to the end of the line, except when `#` appears inside a quoted scalar.

```korml
%!korml version 1.0
---
# document-level comment
name: example  # trailing comment
...
```

Comments are not document-model values, but they are part of the concrete syntax tree.
A round-trip preserving implementation must retain them.

## Document boundaries

Korml supports explicit document boundaries:

```korml
%!korml version 1.0
---
name: first
...
---
name: second
...
```

`DOC_START` marks the beginning of an explicit document.
`DOC_END` marks the end of an explicit document.
A complete source stream starts with a version directive followed by an explicit document start marker.

## Version directive

A version directive belongs to the stream prefix.
It is metadata about the Korml source stream rather than content of any individual document.

```ebnf
VersionDirective ::= VERSION_DIRECTIVE
VERSION_DIRECTIVE ::= "%!korml" WS "version" WS VersionNumber NEWLINE
VersionNumber ::= Digit+ "." Digit+
```

For Korml v1, a source stream starts with:

```korml
%!korml version 1.0
```

The parser should keep the version directive in the concrete syntax tree and expose it as stream metadata.

## Mapping and sequence punctuation

The block grammar uses:

| Token | Meaning |
| --- | --- |
| `COLON` | separates a mapping key from its value. |
| `DASH_ITEM` | starts a block sequence entry. |

The flow grammar uses:

| Token | Meaning |
| --- | --- |
| `FLOW_SEQUENCE_START` | starts a flow sequence, normally `[`. |
| `FLOW_SEQUENCE_END` | ends a flow sequence, normally `]`. |
| `FLOW_MAPPING_START` | starts a flow mapping, normally `{`. |
| `FLOW_MAPPING_END` | ends a flow mapping, normally `}`. |
| `FLOW_SEPARATOR` | separates entries, normally `,`. |

## Scalar forms

Korml has five scalar token forms:

| Token | Purpose |
| --- | --- |
| `PLAIN_SCALAR` | unquoted scalar text. |
| `SQ_SCALAR` | single-quoted scalar text. |
| `DQ_SCALAR` | double-quoted scalar text. |
| `LITERAL_BLOCK_SCALAR` | literal block scalar. |
| `FOLDED_BLOCK_SCALAR` | folded block scalar. |

The document-model value of a scalar is text.
The source spelling is retained separately by the concrete syntax tree.

### Plain scalars

Plain scalars are useful for simple values:

```korml
name: example
enabled: true
count: 3
```

The values above are language-level text values.
A schema or decoding layer may later interpret them as booleans, integers, or other application types.

### Quoted scalars

Single-quoted and double-quoted scalars are used when the source spelling needs explicit quoting:

```korml
single: 'literal text'
double: "escaped text"
```

The exact escaping rules belong to the scalar-token specification and should be tested at the lexer level.

### Block scalars

Literal and folded block scalars are block scalar forms:

```korml
literal: |
  first line
  second line

folded: >
  first line
  second line
```

Block scalar source spelling is part of the concrete syntax tree.
The semantic scalar value is text.
