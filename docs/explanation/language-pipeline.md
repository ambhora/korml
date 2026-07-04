<!--
SPDX-License-Identifier: Apache-2.0
-->

# Language Pipeline

Korml should be described as a language pipeline rather than as only a data model.

A useful conceptual pipeline is:

```text
source text -> tokens -> CST -> semantic view -> schema/application model
```

In previous design discussions this was also described as:

```text
KS -> CST -> KST -> KDM
```

where the important point is the separation between concrete syntax and semantic data.

## Source text

The source text is the original Korml input.
It contains all syntax, comments, spacing, and line endings.

## Tokens

The lexer converts source text into tokens such as:

- scalar tokens,
- comment tokens,
- whitespace tokens,
- punctuation tokens,
- version-envelope tokens where the version supports them,
- layout information.

Tokens are primarily an internal layer of the language implementation.
They are nevertheless useful for specifying the grammar clearly.

## Concrete syntax tree

The parser consumes tokens and builds a concrete syntax tree.
The CST is full-fidelity: it retains enough information to reconstruct the original source text.

This is the right layer for tools that need precise source locations or formatting-preserving edits.

## Semantic view

The semantic view presents the useful document values:

- stream,
- documents,
- mappings,
- sequences,
- scalars.

This view is easier to work with than the CST but is not enough by itself for exact round-tripping.

## Schema or application model

Application-specific typing belongs above the language core.
For example, an application may decide that:

```korml
count: 3
enabled: true
```

means an integer count and a boolean enabled flag.
That interpretation is outside the core grammar.
