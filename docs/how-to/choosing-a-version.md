<!--
SPDX-License-Identifier: Apache-2.0
-->

# Choosing a Korml Version

Use v0 for simple configuration files that contain exactly one document and should remain compatible with the restricted YAML/JSON-shaped subset.

```korml
name: example
runtime:
  ranks: 4
```

v0 is the right default when the file should look like a small ordinary YAML-style configuration file: no Korml version directive, no explicit document markers, and no multi-document stream.

Use v1 when a source needs any of these features:

- an explicit Korml version directive;
- more than one document in the same source text;
- a versioned Korml stream envelope around one or more document bodies.

```korml
%!korml version 1.0
---
name: first
...
---
name: second
...
```

A useful compatibility rule is:

- complete v0 sources are the YAML-compatible single-document subset;
- v1 sources reuse the same body grammar, but the complete source is a Korml stream.

To move a v0 document body into a v1 stream, add the v1 version directive and document boundaries around it.
