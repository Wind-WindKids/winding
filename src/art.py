# @artifact (@art, @a) would generate an artifact from a specified winding
# @art path

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
    for i, data in enumerate(img.data):
        image_bytes = base64.b64decode(data.b64_json)
        if i > 0: filename = filename.replace(".png", f"_{i}.png")
        with open(filename, "wb") as f:
            f.write(image_bytes)

def flatten_winding_to_md(node: Winding, header = True) -> str:
    """
    Convert a Winding AST node back into a markdown snippet
    (header + nested content) suitable as an image prompt.
    """
    lines = []
    if header:
        header = "--\n" + f"{node.at}: {', '.join(node.arguments)}" + "\n--\n"
        lines.append(header)

    # content: serialize Markdown and nested windings
    for item in node.windings:
        if isinstance(item, Winding):
            # nested directive: inline form
            lines.append(f"@{item.at}: {', '.join(item.arguments)}\n")
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

def infer_winding_size(args, page: Winding) -> str:
    """Determine the appropriate size based on arguments."""
    if "landscape" in page.arguments or "spread" in page.arguments:
        return args.landscape
    elif "portrait" in page.arguments:
        return args.portrait
    elif "square" in page.arguments:
        return args.square
    elif ["portrait-" in a for a in page.arguments]:
        return args.portrait
    elif ["landscape-" in a for a in page.arguments]:
        return args.landscape
    
    return None

def generate_image(args, winding: Winding, context: Winding, client: OpenAI):
        prompt_snippet = flatten_winding_to_md(winding)
        context_snippet = flatten_winding_to_md(context, header=False)
        outpath = os.path.join(args.outdir, "images", f"{winding.at}.png")

        print(f"Generating image for winding '{winding.at}' with prompt:\n{prompt_snippet}\n{context_snippet}")
        if args.dry_run:
            print(f"Would save to {outpath}")
            return

        winding_size = infer_winding_size(args, winding)
        if winding_size is None:
            raise ValueError(f"Could not infer size for winding '{winding.at}', unable to generate image.")
            

        # 4. Generate image
        img = client.images.edit(
            model=args.model,
            image=[ open("samples/sophieandwind/images/pages/winter/ice_cream_shop.png","rb"),
                    open("samples/sophieandwind/images/pages/winter/eGull.png", "rb"),
                open("samples/sophieandwind/images/pages/winter/the_rule.png", "rb"),],
                    #open("samples/sophieandwind/images/pages/winter/you_can_fly.png", "rb")],
            prompt="Illuminate in a charming watercolor style.\n" + prompt_snippet,
            n=args.n,
            size=winding_size,
            quality=args.quality,
            input_fidelity="low",
            background="opaque",
        )
        save_img(img, outpath)
        print(f"Saved {outpath}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate an artifact from a specified Winding Markdown path"
    )
    parser.add_argument("input", help="Path to the .md file")
    parser.add_argument("--at", help="Winding path (e.g. 'page', 'page:1', 'chapter:intro')")
    parser.add_argument("--context", type=str, help="Context to prepend to the prompt", default="metadata")
    parser.add_argument("--outdir", help="Output directory", default="tmp")
    parser.add_argument("--generate", action="store_true", help="Generate images")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate all images, even if they exist")
    parser.add_argument("--dry-run", action="store_true", help="Do not generate images, just print what would be done")
    parser.add_argument("--limit", type=int, default=2, help="Limit the number of images to generate (0 for no limit)")
    parser.add_argument("--model", type=str, default="gpt-image-1", help="OpenAI image model to use")
    parser.add_argument("--quality", type=str, default="high", choices=["low", "medium", "high"], help="Quality of generated images")
    parser.add_argument("--portrait", type=str, default="1024x1536", help="Size for portrait images")
    parser.add_argument("--landscape", type=str, default="1536x1024", help="Size for landscape images")
    parser.add_argument("--square", type=str, default="1024x1024", help="Size for square images")
    parser.add_argument("--api-key", type=str, default=os.getenv("OPENAI_API_KEY"), help="OpenAI API key (or set OPENAI_API_KEY env variable)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--debug", action="store_true", help="Debug output")
    parser.add_argument("--n", type=int, default=1, help="Number of images to generate per prompt")


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
    #print(f"Parsed AST from {args.input}:")
    #pprint(ast, indent=2, width=160)

    # 2. Walk & print only the `.at` fields with indentation
    def walk(node: Winding, depth: int = 0):        
        if isinstance(node, Winding):
            yield depth, node
            # chain.from_iterable to flatten child iterators
            child_iters = (walk(child, depth + 1) for child in node.windings)
            yield from chain.from_iterable(child_iters)

    #print("Parsed Winding AST:")
    for depth, node in walk(ast):
        print(f"{'  ' * depth}- {node.at}")    

    # 1.0 Find the fragment if specified
    #if "" in args.input:
    #    node = args.input.split(":")[-1]
    images = []
    context = None
    print(f"Searching for fragment '{node}' in the document...")
    for _, node in walk(ast):
        if node.at == args.at:
            images.append(node)
            print(f"Found fragment '{node.at}' in the document.")
        if node.at == args.context:
            context = node
            print(f"Found context '{node.at}' in the document.")

    

    # 2.1 Identify image nodes
    #images = [
    #    node for node in ast.windings
    #    if isinstance(node, Winding)
    #    and any(attr in ("image", "png", "jpg", "jpeg") for attr in node.arguments)
    #]
    #print(f"Found {len(images)} images in the document at the top level.")
    print("Image:", flatten_winding_to_md(images[0]))
    #return


    if args.generate or args.regenerate:
        client = OpenAI()

        # 3. Generate images
        os.makedirs(os.path.join(args.outdir, "images"), exist_ok=True)

        # 3.1 Generate images for each page
        generated = 0
        for image in images:
            outpath = os.path.join(args.outdir, "images", f"{image.at}.png")
            if os.path.exists(outpath):
                print(f"Skipping existing {outpath}")
                continue

            # Generate the image
            generate_image(args, image, context, client)
            generated += 1

            if args.limit > 0 and generated >= args.limit:
                print(f"Reached limit of {args.limit} images, stopping.")

                return




if __name__ == "__main__":
    main()