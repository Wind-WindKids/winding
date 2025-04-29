from PIL import Image
import numpy as np
from scipy.ndimage import label
from shapely.geometry import MultiPoint
import math, time


def detect_transparent_regions(base_rgba: Image.Image) -> list[dict]:
    start = time.time()
    print(start, "Entering detect_transparent_regions")
    alpha = np.array(base_rgba.split()[-1])
    print(time.time() - start, "Alpha channel extracted")
    mask = alpha < 10
    print(time.time() - start, "Mask created")
    labels, num = label(mask)
    print(time.time() - start, "Labels created")

    def order_points(pts):
        pts = np.array(pts)
        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1).ravel()
        tl = pts[np.argmin(s)]
        br = pts[np.argmax(s)]
        tr = pts[np.argmin(diff)]
        bl = pts[np.argmax(diff)]
        return [tuple(tl), tuple(tr), tuple(br), tuple(bl)]

    transparent_regions = []
    for rid in range(1, num + 1):
        print(time.time() - start, f"Starting processing region {rid}")
        coords = np.column_stack(np.nonzero(labels == rid))
        pts = [(c[1], c[0]) for c in coords]
        print(time.time() - start, f"Coordinates for region {rid} extracted")
        mrr = MultiPoint(pts).minimum_rotated_rectangle
        print(time.time() - start, f"Minimum rotated rectangle for region {rid} calculated")
        rect = list(mrr.exterior.coords)[:-1]
        tl, tr, br, bl = order_points(rect)

        width = math.hypot(tr[0] - tl[0], tr[1] - tl[1])
        height = math.hypot(bl[0] - tl[0], bl[1] - tl[1])
        angle = math.degrees(math.atan2(tr[1] - tl[1], tr[0] - tl[0]))
        centroid = MultiPoint(pts).centroid
        
        orientation = 'landscape' if width > height * 1.25 else \
                      'portrait' if height > width * 1.25 else 'square'   

        transparent_regions.append({
            'coords': pts,
            'width': int(width + 0.5),
            'height': int(height + 0.5),
            'angle': angle,
            'centroid': {'x': centroid.x, 'y': centroid.y},
            'orientation': orientation
        })
        print(time.time() - start, f"Region {rid} processed")


    transparent_regions.sort(key=lambda r: (r['centroid']['y'], r['centroid']['x']))
    print(time.time() - start, "Regions sorted")
    return transparent_regions

def calculate_orientations(patch_paths: list[str]) -> list[str]:
    orientations = []
    for patch_path in patch_paths:
        patch = Image.open(patch_path)
        w, h = patch.size
        if w > h * 1.25:
            orientations.append('landscape')
        elif h > w * 1.25:
            orientations.append('portrait')
        else:
            orientations.append('square')
    return orientations


def fill_transparent_frames(
        base_path: str,
        patch_paths: list[str],
        target_width: int = -1,
        target_height: int = -1,
        reorder_by_orientation: bool = True,
    ) -> Image.Image:

    start = time.time()
    print(start, "Starting fill_transparent_frames")
    base_rgba = Image.open(base_path).convert('RGBA')
    if target_width > 0 and target_height <= 0:
        target_height = int(base_rgba.height * target_width / base_rgba.width + 0.5)
    elif target_height > 0 and target_width <= 0:
        target_width = int(base_rgba.width * target_height / base_rgba.height + 0.5)

    if target_width > 0:
        print(time.time() - start, f"Resizing base image to {target_width}x{target_height}")
        base_rgba = base_rgba.resize((target_width, target_height), Image.LANCZOS)


    transparent_regions = detect_transparent_regions(base_rgba)
    if len(transparent_regions) != len(patch_paths):
        raise ValueError(f"{len(transparent_regions)} frames detected but {len(patch_paths)} patches provided")
    
    if reorder_by_orientation:
        matched_regions = []
        for orientation in calculate_orientations(patch_paths):
            candidates = [r for r in transparent_regions if r['orientation'] == orientation and r not in matched_regions]
            if not candidates:
                raise ValueError(f"No matching transparent region for patch with orientation {orientation}")
            matched_regions.append(candidates[0])
        transparent_regions = matched_regions


    composite = base_rgba.convert('RGB').copy()
    print(time.time() - start, "Base image converted to RGB for pasting patches")

    for region, patch_path in zip(transparent_regions, patch_paths):
        print(time.time() - start, f"Processing region with centroid {region['centroid']} and patch")   
        patch = Image.open(patch_path).convert('RGBA')
        patch_rs = patch.resize((region['width'], region['height']), Image.LANCZOS)
        patch_rot = patch_rs.rotate(-region['angle'], expand=True)

        px = int(region['centroid']['x'] - patch_rot.width / 2)
        py = int(region['centroid']['y'] - patch_rot.height / 2)
        composite.paste(patch_rot.convert('RGB'), (px, py), patch_rot.split()[-1])

        print(time.time() - start, f"Patch pasted at ({px}, {py})")

    print(time.time() - start, "All patches pasted")

    return composite

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Fill transparent frames with images")
    parser.add_argument('base_img', type=str, help='Path to the base image')
    parser.add_argument('patches', type=str, nargs='+', help='Paths to the patch images')
    parser.add_argument('--output', type=str, help='Path to save the output image')
    parser.add_argument('--reorder', action='store_true', help='Reorder patches by orientation')
    parser.add_argument('--width', type=int, default=-1, help='Width of target image')
    parser.add_argument('--height', type=int, default=-1, help='Height of target image')
    args = parser.parse_args()

    result = fill_transparent_frames(args.base_img, args.patches, args.width, args.height, args.reorder)
    if args.output:
        result.save(args.output)
    else:
        result.show()
