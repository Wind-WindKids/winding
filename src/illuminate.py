# 1. **Modify the Story**  
#    Edit the story in `winding.md` to suit your vision. You can adjust the text, images, and layout to make it uniquely yours.

# 2. **Run the Illuminate Script**  
#    Use `illuminate.py` to process the `.md` file. The script will prompt the model to parse the semi-formal markdown, iteratively illuminate the content, and refine the pages until they look just right.

# 3. **Select and Iterate**  
#    Review the generated pages, delete the ones you don't like, and iterate as needed. The process is flexible, allowing you to delete the output during the generation. or ofline, until you're satisfied.

# 4. **Generate the Final Output**  
#    Once the pages are ready, you can use another `.md` file with the page image links to display the content. The script also supports PDF output for printing.


#!/usr/bin/env python3
"""
illuminate.py

Basic scaffolding to:
1. Parse a Winding Markdown file
2. Identify pages/spreads
3. For each page, flatten its AST back to a markdown snippet
4. Generate images via OpenAI and save them

Usage:
    python illuminate.py input.md --outdir output_folder
"""

import argparse
import os
import base64
from pprint import pprint
from itertools import chain

from winding.parser import Lark_StandAlone
from winding.transformer import WindingTransformer
from winding.ast import Winding

from openai import OpenAI

def save_img(img, filename: str):
    """Decode base64-encoded image and write to file."""
    image_bytes = base64.b64decode(img.data[0].b64_json)
    with open(filename, "wb") as f:
        f.write(image_bytes)

def flatten_winding_to_md(node: Winding) -> str:
    """
    Convert a Winding AST node back into a markdown snippet
    (header + nested content) suitable as an image prompt.
    """
    lines = []
    # header fence
    header = "--\n" + f"{node.at}: {', '.join(node.attributes)}" + "\n--\n"
    lines.append(header)
    # content: serialize Markdown and nested windings
    for item in node.content:
        if isinstance(item, Winding):
            # nested directive: inline form
            lines.append(f"@{item.at}: {', '.join(item.attributes)}\n")
            # flatten its content recursively (only text/images)
            lines.append(flatten_winding_to_md(item).split("--\n")[-1])
        else:
            # Markdown or Image represented as its content text
            # assume item.content holds either str or nested Image AST
            text = getattr(item, "content", str(item))
            if hasattr(text, "caption"):
                # might be an Image AST
                text = f"![{text.caption}]({text.url})\n"
            else:
                text = str(text)
            lines.append(text)
    return "".join(lines)

def infer_page_size(args, page: Winding) -> str:
    """Determine the appropriate page size based on attributes."""
    if "landscape" in page.attributes or "spread" in page.attributes:
        return args.landscape
    elif "portrait" in page.attributes:
        return args.portrait
    elif "square" in page.attributes:
        return args.square
    elif ["portrait-" in a for a in page.attributes]:
        return args.portrait
    elif ["landscape-" in a for a in page.attributes]:
        return args.landscape


    return None

def main():
    parser = argparse.ArgumentParser(
        description="Illuminate Winding Markdown pages via OpenAI image generation"
    )
    parser.add_argument("input", help="Path to the .md file")
    parser.add_argument("--outdir", default="images/", help="Directory to save generated images")
    parser.add_argument("--model", default="gpt-image-1", help="Image generation model")
    parser.add_argument("--landscape", default="1536x1024", help="Landscape image size (e.g., 1536x1024)")
    parser.add_argument("--portrait", default="1024x1536", help="Portrait image size (e.g., 1024x1536)")
    parser.add_argument("--square", default="1024x1024", help="Square image size (e.g., 1024x1024)")
    parser.add_argument("--quality", default="high", help="Image quality setting")
    parser.add_argument("--dry-run", action="store_true", help="Skip image generation, just parse and print")
    args = parser.parse_args()

    # 1. Load and parse
    with open(args.input, "r") as f:
        text = f.read()
    parser_ = Lark_StandAlone()
    try:
        tree    = parser_.parse(text)
    except Exception as e:
        msg = f"\nFile {args.input}, line {e.line}, column {e.column}: Syntax Error\n"
        msg += e.get_context(text)
        print(msg)
        return


    ast = WindingTransformer().transform(tree)

    # 2. Walk & print only the `.at` fields with indentation
    def walk(node: Winding, depth: int = 0):        
        if isinstance(node, Winding):
            yield depth, node.at
            # chain.from_iterable to flatten child iterators
            child_iters = (walk(child, depth + 1) for child in node.content)
            yield from chain.from_iterable(child_iters)

    #print("Parsed Winding AST:")
    #for depth, at in walk(ast):
    #    print(f"{'  ' * depth}- {at}")    

    #pprint(ast.content[0].content[2].content[0].at)



    # 2. Identify page/spread nodes
    pages = [
        node for node in ast.content
        if isinstance(node, Winding)
        and any(attr in ("page", "spread") for attr in node.attributes)
    ]

    # 3. Process each page
    client = OpenAI()
    for page in pages:
        filename = f"{page.at}.png"
        outpath  = os.path.join(args.outdir, filename)
        if os.path.exists(outpath):
            print(f"Skipping existing {filename}")
            continue

        prompt_snippet = flatten_winding_to_md(page)
        print(f"Generating image for page '{page.at}' with prompt:\n{prompt_snippet}")
        if args.dry_run:
            print(f"Would save to {outpath}")
            continue

        page_size = infer_page_size(args, page)
        if page_size is None:
            print(f"Warning: No size specified for page '{page.at}'. Skipping for now.")
            continue

        # 4. Generate image
        img = client.images.generate(
            model=args.model,
            prompt=prompt_snippet,
            n=1,
            size=page_size,
            quality=args.quality
        )
        save_img(img, outpath)
        print(f"Saved {outpath}")

if __name__ == "__main__":
    main()
