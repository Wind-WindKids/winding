from PIL import Image
import numpy as np
from scipy.ndimage import label
from shapely.geometry import MultiPoint
import math
import matplotlib.pyplot as plt

def fill_transparent_frames(
        base_path: str,
        patch_paths: list[str]
    ) -> Image.Image:
    base_rgba = Image.open(base_path).convert('RGBA')
    w, h = base_rgba.size
    alpha = np.array(base_rgba.split()[-1])
    mask = alpha < 10
    labels, num = label(mask)
    if len(patch_paths) != num:
        raise ValueError(f"{num} frames detected but {len(patch_paths)} patches provided")
    composite = base_rgba.convert('RGB').copy()

    def order_points(pts):
        pts = np.array(pts)
        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1).ravel()
        tl = pts[np.argmin(s)]
        br = pts[np.argmax(s)]
        tr = pts[np.argmin(diff)]
        bl = pts[np.argmax(diff)]
        return [tuple(tl), tuple(tr), tuple(br), tuple(bl)]

    for rid in range(1, num + 1):
        coords = np.column_stack(np.nonzero(labels == rid))
        pts = [(c[1], c[0]) for c in coords]
        mrr = MultiPoint(pts).minimum_rotated_rectangle
        rect = list(mrr.exterior.coords)[:-1]
        tl, tr, br, bl = order_points(rect)

        width = math.hypot(tr[0] - tl[0], tr[1] - tl[1])
        height = math.hypot(bl[0] - tl[0], bl[1] - tl[1])
        angle = math.degrees(math.atan2(tr[1] - tl[1], tr[0] - tl[0]))

        patch = Image.open(patch_paths[rid - 1]).convert('RGBA')
        patch_rs = patch.resize((int(width), int(height)), Image.LANCZOS)
        patch_rot = patch_rs.rotate(-angle, expand=True)

        centroid = MultiPoint(pts).centroid
        px = int(centroid.x - patch_rot.width / 2)
        py = int(centroid.y - patch_rot.height / 2)

        composite.paste(patch_rot.convert('RGB'), (px, py), patch_rot.split()[-1])

    return composite

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Fill transparent frames with images")
    parser.add_argument('base_img', type=str, help='Path to the base image')
    parser.add_argument('patches', type=str, nargs='+', help='Paths to the patch images')
    args = parser.parse_args()

    result = fill_transparent_frames(args.base_img, args.patches)
    result.show()
