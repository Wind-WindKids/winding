import os

grammar = r"""start: (winding | markdown)+

winding: meta_winding | space_winding | inline_winding
meta_winding: "===\n" receivers ":" arguments header_winding* "\n===\n" windings? 
space_winding: "--\n" receivers ":" arguments header_winding* "\n--\n" windings?
header_winding: "\n" receivers ":" arguments
inline_winding: "@" receivers ":" arguments "\n" markdown?

windings: (inline_winding | markdown)+
markdown: (image | TEXT)+
image: "![" CAPTION? "]" "(" URI? ")"

receivers: IDENTIFIER ("," IDENTIFIER)*
arguments: (IDENTIFIER ("," IDENTIFIER)*)?


IDENTIFIER: /!?[A-Za-z0-9][ A-Za-z0-9_.-]*/
URI: /[^\)\n]+/
TEXT: /(?:(?!@\w+[A-Za-z0-9_.,-]*:|--|===|!\[).)*\n+/ 
CAPTION: /[^\]]+/
    
%ignore /[ \t]+/
%ignore "\r"  
"""
