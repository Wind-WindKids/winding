#!/usr/bin/env python3
"""
typeset.py

A simple script to convert Winding Markdown into a LaTeX document using PyLaTeX.
Interprets basic tags: pages and spreads, text, and images.
"""

import argparse
from pylatex import Document, Section, NoEscape, Figure
from pylatex.utils import escape_latex

from winding.parser import Lark_StandAlone
from winding.transformer import WindingTransformer
from winding.ast import Winding, Markdown
from winding.ast import Image as ASTImage

def render_content(item, doc: Document):
    """Render a single AST item into the PyLaTeX document."""
    if isinstance(item, Markdown):
        content = item.content
        if isinstance(content, ASTImage):
            # Render an image
            img = content
            with doc.create(Figure(position='h!')) as fig:
                fig.add_image(img.url, width=NoEscape(r'0.8\textwidth'))
                fig.add_caption(escape_latex(img.caption))
        else:
            # Render text (escape LaTeX special chars)
            text = escape_latex(str(content))
            doc.append(NoEscape(text + "\n\n"))
    elif isinstance(item, Winding):
        # Nested directives: treat as subsection
        title = escape_latex(item.at)
        with doc.create(Section(title, numbering=False)):
            for child in item.content:
                render_content(child, doc)

def main():
    parser = argparse.ArgumentParser(
        description="Convert Winding Markdown (.md) to LaTeX using PyLaTeX"
    )
    parser.add_argument("input", help="Path to the .md file")
    parser.add_argument("--output", "-o", default="output.tex", help="Output .tex filename")
    args = parser.parse_args()

    # Parse input file
    text = open(args.input, "r").read()
    lark_parser = Lark_StandAlone()
    tree = lark_parser.parse(text)
    ast = WindingTransformer().transform(tree)

    # Create LaTeX document
    doc = Document(documentclass="book")
    doc.preamble.append(NoEscape(r"\usepackage{graphicx}"))
    doc.preamble.append(NoEscape(r"\usepackage[margin=1in]{geometry}"))

    # Iterate over top-level pages/spreads
    for node in ast.content:
        if not isinstance(node, Winding):
            continue
        if "page" in node.attributes or "spread" in node.attributes:
            # start new page
            doc.append(NoEscape(r"\clearpage"))
            title = escape_latex(node.at.replace("_", " ").title())
            # Add a section for the page
            doc.append(NoEscape(r"\section*{" + title + "}"))
            # Render children
            for item in node.content:
                render_content(item, doc)

    # Generate .tex file
    doc.generate_tex(args.output.replace(".tex", ""))
    print(f"Wrote LaTeX to {args.output}")

if __name__ == "__main__":
    main()
