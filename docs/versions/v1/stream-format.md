<!--
SPDX-License-Identifier: Apache-2.0
-->

# Stream Format

Korml v1 is a versioned stream format.
The stream envelope is the part that distinguishes a complete v1 source from a v0 source.

A v1 source starts with a Korml version directive:

```korml
%!korml version 1.0
```

Each document then starts with an explicit document boundary:

```korml
---
name: example
...
```

A complete v1 source therefore looks like this:

```korml
%!korml version 1.0
---
name: first
...
---
name: second
...
```

The document bodies use the same restricted mapping/sequence/scalar grammar as v0.
That means existing v0 document bodies can be placed inside a v1 stream without changing their document values.

## Compatibility boundary

The YAML-compatible source form is v0, because v0 is exactly one implicit document with no Korml-specific stream header.

v1 is different:

- `%!korml version 1.0` is Korml source metadata;
- `---` starts each Korml stream document;
- `...` may end a document explicitly;
- one source may contain more than one document.

Therefore, a complete v1 source should be treated as a Korml stream, not as the YAML-compatible single-document subset.
