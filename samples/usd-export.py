#!/usr/bin/env python3
"""
usd_export.py

Convert a Winding Markdown file into an OpenUSD stage.
Each page/spread becomes an Xform prim; text and images become child prims
with custom attributes for content, image paths, or directives.
"""

import argparse
import re
from pxr import Usd, UsdGeom, Sdf

from winding.parser import Lark_StandAlone
from winding.transformer import WindingTransformer
from winding.ast import Winding, Markdown, Image as ASTImage

def sanitize_name(name: str) -> str:
    """Make a valid USD prim name from an arbitrary string."""
    # Replace invalid characters with underscore, ensure starts with letter
    s = re.sub(r'[^A-Za-z0-9_]', '_', name)
    if not re.match(r'[A-Za-z]', s):
        s = "N" + s
    return s

def find_pages(node: Winding) -> list[Winding]:
    """Recursively gather all Winding nodes with attribute 'page' or 'spread'."""
    pages = []
    if 'page' in node.attributes or 'spread' in node.attributes:
        pages.append(node)
    for c in node.content:
        if isinstance(c, Winding):
            pages.extend(find_pages(c))
    return pages

def export_to_usd(ast: Winding, out_usd: str):
    """Build a USD stage from the Winding AST and save to file."""
    stage = Usd.Stage.CreateNew(out_usd)
    # Create a top-level root
    root = UsdGeom.Xform.Define(stage, '/Root')
    stage.SetDefaultPrim(root.GetPrim())

    pages = find_pages(ast)
    for pg in pages:
        # Create a prim for this page/spread
        pg_name = sanitize_name(pg.at)
        pg_path = f"/Root/{pg_name}"
        pg_xform = UsdGeom.Xform.Define(stage, pg_path)

        # Store attributes list as metadata
        attr_list = pg_xform.GetPrim().CreateAttribute(
            'winding:attributes', Sdf.ValueTypeNames.StringArray)
        attr_list.Set(pg.attributes)

        # Iterate over page content
        for idx, item in enumerate(pg.content):
            child_name = f"{pg_name}_item{idx}"
            child_path = f"{pg_path}/{sanitize_name(child_name)}"
            if isinstance(item, ASTImage):
                # Direct ASTImage at top-level (rare case)
                imgprim = UsdGeom.Xform.Define(stage, child_path)
                imgattr = imgprim.GetPrim().CreateAttribute(
                    'winding:imagePath', Sdf.ValueTypeNames.String)
                imgattr.Set(item.url)
                # store caption too
                capattr = imgprim.GetPrim().CreateAttribute(
                    'winding:caption', Sdf.ValueTypeNames.String)
                capattr.Set(item.caption)
            elif isinstance(item, Markdown):
                content = item.content
                if isinstance(content, ASTImage):
                    # image inside Markdown
                    imgprim = UsdGeom.Xform.Define(stage, child_path)
                    imgprim.GetPrim().CreateAttribute(
                        'winding:imagePath', Sdf.ValueTypeNames.String
                    ).Set(content.url)
                    imgprim.GetPrim().CreateAttribute(
                        'winding:caption', Sdf.ValueTypeNames.String
                    ).Set(content.caption)
                else:
                    # plain text
                    txtprim = UsdGeom.Xform.Define(stage, child_path)
                    txtprim.GetPrim().CreateAttribute(
                        'winding:text', Sdf.ValueTypeNames.String
                    ).Set(str(content))
            elif isinstance(item, Winding):
                # nested directive
                sub_name = sanitize_name(item.at)
                sub_path = f"{pg_path}/{sub_name}_{idx}"
                subprim = UsdGeom.Xform.Define(stage, sub_path)
                subprim.GetPrim().CreateAttribute(
                    'winding:directive', Sdf.ValueTypeNames.String
                ).Set(item.at)
                subprim.GetPrim().CreateAttribute(
                    'winding:attributes', Sdf.ValueTypeNames.StringArray
                ).Set(item.attributes)
                # No further nesting for simplicity
    stage.GetRootLayer().Save()

def main():
    parser = argparse.ArgumentParser(
        description="Export Winding Markdown to USD scene graph"
    )
    parser.add_argument("input", help="Path to the .md file")
    parser.add_argument("--output", "-o", default="scene.usda",
                        help="Output USD file path")
    args = parser.parse_args()

    text = open(args.input, "r").read()
    # Parse and transform
    parser_ = Lark_StandAlone()
    tree    = parser_.parse(text)
    ast     = WindingTransformer().transform(tree)

    export_to_usd(ast, args.output)
    print(f"USD scene written to {args.output}")

if __name__ == "__main__":
    main()

