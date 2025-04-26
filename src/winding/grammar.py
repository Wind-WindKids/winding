import os

grammar = r"""start: (winding | markdown)+

winding: space_winding | inline_winding
space_winding: "--" NEWLINE IDENTIFIER ":" attributes NEWLINE "--" NEWLINE content?
inline_winding: "@" IDENTIFIER ":" attributes NEWLINE content?

content: (winding | markdown)+

markdown: (image | TEXT_LINE | NEWLINE)+

attributes: (IDENTIFIER ("," IDENTIFIER)*)?

image: "![" IDENTIFIER "]" "(" URI ")"

IDENTIFIER: /!?[A-Za-z][A-Za-z0-9_.-]*/
URI: /[^\)\n]+/
TEXT_LINE: /[^\n@!-][^\n]*/

NEWLINE: /\r?\n/

%ignore /[ \t]+/
"""