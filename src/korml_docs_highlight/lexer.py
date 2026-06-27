# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# --------------------------------------------------------------------------------------------------

"""Pygments lexer for Korml examples in the language specification docs."""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Keyword, Name, Number, Punctuation, String, Text


class KormlLexer(RegexLexer):
    """A small lexer for Korml documentation examples.

    This lexer is intentionally documentation-oriented. It highlights the stable
    surface syntax used in the language specification without trying to perform
    full parsing or schema-level interpretation.
    """

    name = "Korml"
    aliases = ["korml"]
    filenames = ["*.korml"]
    mimetypes = ["text/x-korml"]

    tokens = {
        "root": [
            # Korml stream header.
            (
                r"^(%!korml)(\s+)(version)(\s+)([0-9]+(?:\.[0-9]+)*)",
                bygroups(Comment.Preproc, Text.Whitespace, Keyword, Text.Whitespace, Number),
            ),
            # YAML-like document boundary markers used by Korml.
            (r"^(\s*)(---|\.\.\.)(\s*)$", bygroups(Text.Whitespace, Punctuation, Text.Whitespace)),
            # Comments.
            (r"#.*$", Comment.Single),
            # Indentation and other whitespace.
            (r"\s+", Text.Whitespace),
            # Block sequence marker.
            (r"(-)(\s+)", bygroups(Punctuation, Text.Whitespace)),
            # Mapping keys. This intentionally covers the simple key form used
            # throughout the language-spec examples.
            (r"([A-Za-z_][A-Za-z0-9_.-]*)(\s*)(:)", bygroups(Name.Tag, Text.Whitespace, Punctuation)),
            # Flow collection punctuation.
            (r"[\[\]\{\},]", Punctuation),
            # Block scalar indicators.
            (r"[|>][-+]?", String.Doc),
            # Quoted scalars.
            (r'"([^"\\]|\\.)*"', String.Double),
            (r"'([^']|'')*'", String.Single),
            # Everything else is a plain scalar fragment. Korml keeps typing out
            # of the core grammar, so these are not highlighted as booleans,
            # integers, floats, or nulls.
            (r"[^#\s\[\]\{\},:]+", String),
            (r".", Text),
        ]
    }
