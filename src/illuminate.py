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
from PIL import Image
from patching import detect_transparent_regions, fill_transparent_frames

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

def infer_winding_size(args, page: Winding) -> str:
    """Determine the appropriate size based on attributes."""
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

def generate_image(args, winding: Winding, client: OpenAI):
        prompt_snippet = flatten_winding_to_md(winding)
        outpath = os.path.join(args.outdir, "images", f"{winding.at}.png")

        print(f"Generating image for winding '{winding.at}' with prompt:\n{prompt_snippet}")
        if args.dry_run:
            print(f"Would save to {outpath}")
            return

        winding_size = infer_winding_size(args, winding)
        if winding_size is None:
            raise ValueError(f"Could not infer size for winding '{winding.at}', unable to generate image.")
            

        # 4. Generate image
        img = client.images.generate(
            model=args.model,
            prompt=prompt_snippet,
            n=1,
            size=winding_size,
            quality=args.quality
        )
        save_img(img, outpath)
        print(f"Saved {outpath}")


def export(args, pages):
    """Export the pages as a set of png files."""
    os.makedirs(os.path.join(args.outdir, "export"), exist_ok=True)

    page_number = 1
    for page in pages:
        image_path  = os.path.join(args.outdir, "pages", f"{page.at}.png")
        patched_path = os.path.join(args.outdir, "pages", f"{page.at}.patched.png")
        if os.path.exists(patched_path):
            image_path = patched_path
        elif not os.path.exists(image_path):
            print(f"Error: {image_path} not found, skipping.")
            break

        # Read the image, check if the orientation is portrait
        # if yes, simpy copy the image to the export folder
        image = Image.open(image_path).convert("RGB")
        if image.width < image.height:
            # Portrait image, save it without the alpha channel
            cover = next((a for a in page.attributes if a.startswith("cover")), None)
            if cover:
                image.save(os.path.join(args.outdir, "export", f"{cover}.png"))
            else:
                image.save(os.path.join(args.outdir, "export", f"{page_number:03d}.png"))
                page_number += 1
        else:
            # Landscape image, split it into two halves and save each half
            half = image.crop((0, 0, image.width // 2, image.height))
            half.save(os.path.join(args.outdir, "export", f"{page_number:03d}.png"))
            page_number += 1
            half = image.crop((image.width // 2, 0, image.width, image.height))
            half.save(os.path.join(args.outdir, "export", f"{page_number:03d}.png"))
            page_number += 1
    print(f"Exported {page_number} pages to {args.outdir}/export/")
            

        
def export_pdf(args):
    """Combines the exported images into a single PDF file."""
    import glob
    from fpdf import FPDF
    from PIL import Image

    # 0. Get the image paths and check they exist, no skipped images
    exported_images = sorted(glob.glob(os.path.join(args.outdir, "export", "???.png")))
    page_number = len(exported_images)
    for n in range(page_number):
        if not os.path.exists(exported_images[n]):
            print(f"Error: {exported_images[n]} not found, unable to export PDF.")
            return

    # 1. Determine the trim size in inches
    trim_w, trim_h = map(float, args.trim.split("x"))
    bleed = float(args.bleed)
    # 2. Calculate the page size in inches
    page_w = trim_w + bleed
    page_h = trim_h + 2 * bleed
    # 3. Convert to pixels
    image_w = int(page_w * args.dpi + 0.5)
    image_h = int(page_h * args.dpi + 0.5)

    pdf = FPDF(unit="in", format=(page_w, page_h))
    pdf.set_auto_page_break(auto=True, margin=0)
    
    for n in range(page_number):
        image_path = exported_images[n]
        image = Image.open(image_path)
        if image.mode != "RGB" or image.width != image_w or image.height != image_h:
            print(f"Warning: {image_path} is not in RGB mode or does not match the page size.")

        pdf.add_page(orientation="P")
        pdf.rect(0, 0, page_w, page_h, style="DF")
        pdf.image(image_path, 0, 0, w=page_w, h=page_h, keep_aspect_ratio=False)

    # Save the PDF
    pdf_path = os.path.join(args.outdir, "export", "output-32.pdf")
    pdf.output(pdf_path)
    print(f"Exported PDF to {pdf_path}")    


def main():
    parser = argparse.ArgumentParser(
        description="Illuminate Winding Markdown pages via OpenAI image generation"
    )
    parser.add_argument("input", help="Path to the .md file")
    parser.add_argument("--preview", help="Path to save the preview.md file", default="preview.md")
    parser.add_argument("--outdir", default="images/", help="Directory to save generated images")
    parser.add_argument("--model", default="gpt-image-1", help="Image generation model")
    parser.add_argument("--landscape", default="1536x1024", help="Landscape image size (e.g., 1536x1024)")
    parser.add_argument("--portrait", default="1024x1536", help="Portrait image size (e.g., 1024x1536)")
    parser.add_argument("--square", default="1024x1024", help="Square image size (e.g., 1024x1024)")
    parser.add_argument("--trim", default="6x9", help="Physical Trim size in inches (e.g., 4x6)")
    parser.add_argument("--bleed", default="0.125", help="Bleed size in inches (e.g., 0.125)")
    parser.add_argument("--pad", default=12, type=int, help="Padding for the patches")
    parser.add_argument("--dpi", default=300, type=int, help="DPI for the output pages")
    parser.add_argument("--quality", default="high", help="Image quality setting")
    parser.add_argument("--dry-run", action="store_true", help="Skip image generation, just parse and print")
    parser.add_argument("--export", action="store_true", help="Export the pages")
    parser.add_argument("--export-pdf", action="store_true", help="Export the pages as a PDF")
    parser.add_argument("--generate", action="store_true", help="Generate images")
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
    print(f"Found {len(pages)} pages in the document at the top level.")

    # 2.1 Identify image nodes
    images = [
        node for node in ast.content
        if isinstance(node, Winding)
        and any(attr in ("image", "png", "jpg", "jpeg") for attr in node.attributes)
    ]
    print(f"Found {len(images)} images in the document at the top level.")

    # 3.0 Generate preview.md
    with open(args.preview, "w") as f:
        for page in pages:
            outpath  = os.path.join(args.outdir, "pages", f"{page.at}.png")
            patched_path = os.path.join(args.outdir, "pages", f"{page.at}.patched.png")
            if os.path.exists(patched_path):
                outpath = patched_path
            elif not os.path.exists(outpath):
                print(f"Warning: {outpath} not found, skipping.")

            f.write(f"![{page.at}]({outpath})\n")
            f.write(flatten_winding_to_md(page))
            f.write("\n\n")
    
    if args.export:
        export(args, pages)
        return

    if args.export_pdf:
        export_pdf(args)
        return

    if args.generate:
        client = OpenAI()

        # 3. Generate images
        os.makedirs(os.path.join(args.outdir, "images"), exist_ok=True)

        # 3.1 Generate images for each page
        for image in images:
            outpath = os.path.join(args.outdir, "images", f"{image.at}.png")
            if os.path.exists(outpath):
                print(f"Skipping existing {outpath}")
                continue

            # Generate the image
            generate_image(args, image, client)
        return

    #if args.dry_run:
    #    print(f"Preview saved to {args.preview}")
    #    return



    # 3.1 Process each page
    for page in pages:
        outpath  = os.path.join(args.outdir, "pages", f"{page.at}.png")
        patched_path = os.path.join(args.outdir, "pages", f"{page.at}.patched.png")

        if os.path.exists(outpath):
            print(f"Skipping existing {outpath}")
            continue

        if os.path.exists(patched_path):
            print(f"Skipping existing {patched_path}")
            continue


        # Check if there are any cutouts windings
        cutouts = [child for child in page.content if isinstance(child, Winding) and "cutout" in child.attributes]
        if cutouts:
            print(f"Found cutouts in page '{page.at}': {cutouts}")
            transparent_path = os.path.join(args.outdir, "pages", f"{page.at}.transparent.png")

            if not os.path.exists(transparent_path):
                print(f"Transparent image path not found, skipping'{page.at}.transparent.png'")
                continue

            # Get the patch paths
            for cutout in cutouts:
                print(f"Cutout '{cutout.at}' with content: {cutout.content[0].content.url}")
                patch_path = os.path.join(args.outdir, "cutouts", cutout.content[0].content.url)
                if not os.path.exists(patch_path):
                    print(f"Patch {patch_path} not found, skipping '{cutout.at}'")

            
            patch_paths = [os.path.join(args.outdir, "cutouts", cutout.content[0].content.url) for cutout in cutouts]
            existing_patch_paths = [path for path in patch_paths if os.path.exists(path)]

            if len(existing_patch_paths) != len(patch_paths):
                print(f"Warning: {len(patch_paths) - len(existing_patch_paths)} patches not found for '{page.at}'")
                continue

            if len(existing_patch_paths) != len(cutouts):
                print(f"Warning: {len(existing_patch_paths)} patches found, but {len(cutouts)} expected for '{page.at}'")
                continue


            base_rgba = Image.open(transparent_path)
            if base_rgba.mode != 'RGBA':
                print(f"Error: '{page.at}.transparent.png' is not in RGBA mode. Skipping.")
                continue

            transparent_regions = detect_transparent_regions(base_rgba)

            if len(transparent_regions) != len(existing_patch_paths):
                print(f"Warning: {len(transparent_regions)} transparent regions detected, but {len(existing_patch_paths)} patches provided for '{page.at}'")
                continue

            # Determine the target size from the trim, dpi and the page size
            target_width = int((float(args.trim.split("x")[0]) + float(args.bleed)) * args.dpi + 0.5)
            target_height = int((float(args.trim.split("x")[1]) + float(args.bleed) * 2) * args.dpi + 0.5)

            # If the image is landscape, assume this is a spread
            if "spread" in page.attributes:
                target_width *= 2
                if base_rgba.width < base_rgba.height:
                    print(f"Error: '{page.at}.transparent.png' is not in landscape mode. Skipping.")
                    continue
            else:
                if base_rgba.width > base_rgba.height:
                    print(f"Error: '{page.at}.transparent.png' is not in portrait mode. Skipping.")
                    continue

            print(f"Transparent regions detected in '{page.at}.transparent.png' with existing patches: {existing_patch_paths}")
            patched_rgb = fill_transparent_frames(base_rgba, patch_paths, target_width, target_height, reorder_by_orientation=True, pad=args.pad)
            if patched_rgb:
                patched_rgb.save(patched_path)
                print(f"Saved filled transparent regions to '{patched_path}'")
            else:
                print(f"Error: Failed to fill transparent regions for '{page.at}'")

        if args.generate:
            # Generate the image for the page
            generate_image(args, page, client)

if __name__ == "__main__":
    main()
