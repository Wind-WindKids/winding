#!/usr/bin/env python3
"""
import.py

Import arbitrary documents (image, PDF, text) and invoke the OpenAI model to produce a .winding.md file.
Depending on input format, adjusts instructions for parsing into the Winding Markdown schema.
"""
import argparse
import os
import base64
from openai import OpenAI
from typing import List, Union
from pydantic import BaseModel, Field
from winding.grammar import grammar

# Define the Pydantic schema for parsing
class Image(BaseModel):
    caption: str = Field(..., description="Image caption.")
    url: str     = Field(..., description="Image URL.")

class Markdown(BaseModel):
    content: Union[str, 'Markdown', Image] = Field(
        ..., description="Plain text, nested Markdown, or Image node."
    )

class Winding(BaseModel):
    at: str = Field(..., description="The @at recipient, a valid identifier.")
    attributes: List[str] = Field(
        default_factory=list,
        description="Modifiers (e.g., size, orientation, !negation)."
    )
    content: List[Union[Markdown, 'Winding']] = Field(
        default_factory=list,
        description="Child nodes: text (Markdown), or nested directives (Winding)."
    )

# Update forward references
Markdown.update_forward_refs()
Winding.update_forward_refs()


def load_input(path: str) -> tuple[str, dict]:
    """
    Read the input file and return a tuple (mode, payload).
    mode: one of 'text', 'pdf', 'image'
    payload: dict with keys for the parse call (e.g., 'input', 'input_bytes')
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.txt', '.md'):
        data = open(path, 'r', encoding='utf-8').read()
        return 'text', {'input': data}

    if ext == '.pdf':
        try:
            import PyPDF2
        except ImportError:
            raise RuntimeError("PyPDF2 not installed: pip install PyPDF2")
        reader = PyPDF2.PdfReader(path)
        pages = [page.extract_text() for page in reader.pages]
        data = "\n\n".join(pages)
        return 'pdf', {'input': data}

    if ext in ('.png', '.jpg', '.jpeg'):  # image file
        with open(path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        return 'image', {'input_bytes': b64}

    raise ValueError(f"Unsupported extension: {ext}")


def main():
    parser = argparse.ArgumentParser(
        description="Import a document and generate Winding Markdown"
    )
    parser.add_argument('input', help='Path to input file (txt, md, pdf, png, jpg)')
    parser.add_argument('--output', '-o', help='Path to output .winding.md')
    args = parser.parse_args()

    mode, payload = load_input(args.input)
    instructions = "You are given a document, convert it into Winding Markdown following the EBNF grammar."

    if mode == '.md':
        f"Parse the following input into Winding Markdown. If helpful, here is the EBNF grammar: {grammar}",


        "You are given an image.Decompose the scene into the scene graph and interpret it as Winding Markdown."
        if mode == 'image' else
        
    )

    client = OpenAI()
    response = client.responses.parse(
        model="gpt-4o-2024-08-06",
        instructions=
        text_format=Winding,
        **payload
    )

    # Determine output path
    out = args.output or os.path.splitext(args.input)[0] + '.winding.md'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(response)  # assume response is a markdown string
    print(f"Wrote Winding Markdown to {out}")


if __name__ == '__main__':
    main()
