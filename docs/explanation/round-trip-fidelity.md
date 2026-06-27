<!--
SPDX-License-Identifier: Apache-2.0
-->

# Round-trip Fidelity

Round-trip fidelity means that a parser can read a Korml source text and an emitter can write it back without unnecessary changes.

For Korml, round-tripping is a design goal rather than an afterthought.

## Why the document model is not enough

The document model contains only semantic values:

- mappings,
- sequences,
- scalars,
- documents.

It does not contain the syntax details needed to reconstruct the original source text.
For example, the following documents may have the same document-model value but different source spelling:

```korml
name: example
```

```korml
# project name
name : example
```

A plain document model would lose the comment and spacing.

## What must be preserved

A round-trip preserving Korml implementation should preserve:

- comments,
- whitespace,
- blank lines,
- indentation,
- document boundaries,
- scalar spelling,
- quote style,
- block scalar style,
- version directives,
- source spans or token positions.

## Concrete syntax tree

The concrete syntax tree is the source-preserving representation.
It keeps both semantic structure and syntactic details.

A semantic mapping entry such as:

```korml
name: example
```

contains more than the abstract key `name` and value `example`.
The concrete syntax also includes the key token, colon token, whitespace, value token, line ending, and source spans.

## Editing without destroying formatting

The practical benefit of full-fidelity parsing is controlled editing.
A tool can change one value without reformatting the whole document:

```korml
# keep this comment
name: old
```

can become:

```korml
# keep this comment
name: new
```

without losing the comment or changing unrelated layout.
