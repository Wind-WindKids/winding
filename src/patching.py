from PIL import Image
import numpy as np
from scipy.ndimage import label
from shapely.geometry import MultiPoint
import math, time

from scipy.spatial import ConvexHull


# Shapely-equivalent region detection (worked earlier)
def get_region_rect_shapely(labels: np.ndarray, rid: int):
    coords = np.column_stack(np.nonzero(labels == rid))
    pts = coords[:, [1, 0]].astype(float)
    if len(pts) < 32:
        raise ValueError("Region too small to calculate bounding box")
    hull = ConvexHull(pts)
    hull_pts = np.vstack([pts[hull.vertices], pts[hull.vertices][0]])
    edges = hull_pts[1:] - hull_pts[:-1]
    angles = np.unique(np.arctan2(edges[:,1], edges[:,0]))
    best_area = np.inf
    best = (0, 0, 0.0)
    for ang in angles:
        ca, sa = math.cos(-ang), math.sin(-ang)
        R = np.array([[ca, -sa],[sa, ca]])
        rot = pts @ R.T
        min_x, max_x = rot[:,0].min(), rot[:,0].max()
        min_y, max_y = rot[:,1].min(), rot[:,1].max()
        w, h = max_x-min_x, max_y-min_y
        area = w*h
        if area < best_area:
            if w <= h:
                width, height, angle_edge = w, h, ang
            else:
                width, height, angle_edge = h, w, ang + math.pi/2
            best_area = area
            best = (width, height, angle_edge)
    w_opt, h_opt, angle_edge = best
    angle = math.degrees(angle_edge)

    # normalize angle to be between -90 and 90 degrees
    if angle > 90: angle -= 180
    elif angle <= -90: angle += 180

    # remove the nearest 90° chunk and swap width and height if needed
    if abs(angle) > 45:
        angle = angle - 90 * round(angle / 90)
        w_opt, h_opt = h_opt, w_opt


    return int(w_opt+0.5), int(h_opt+0.5), angle

def detect_transparent_regions(base_rgba: Image.Image) -> list[dict]:
    if base_rgba.mode != 'RGBA':
        raise ValueError("Base image must be in RGBA mode")

    alpha = np.array(base_rgba.split()[-1])
    mask = alpha < 10
    labels, num = label(mask)
    regions = []
    for rid in range(1, num+1):
        try:
            width, height, angle = get_region_rect_shapely(labels, rid)
        except ValueError:
            #print(f"Region {rid} too small to calculate bounding box")
            continue
        coords = np.column_stack(np.nonzero(labels == rid))
        pts = coords[:, [1,0]].astype(float)
        centroid = pts.mean(axis=0)
        if width > height * 1.15: orientation = 'landscape'
        elif height > width * 1.15: orientation = 'portrait'
        else: orientation = 'square'
        regions.append({
            'width': width,
            'height': height,
            'angle': angle,
            'centroid': {'x': float(centroid[0]), 'y': float(centroid[1])},
            'orientation': orientation
        })
    regions.sort(key=lambda r:(r['centroid']['y'], r['centroid']['x']))
    return regions

def calculate_orientations(patch_paths: list[str]) -> list[str]:
    orientations = []
    for patch_path in patch_paths:
        patch = Image.open(patch_path)
        w, h = patch.size
        if w > h * 1.15:
            orientations.append('landscape')
        elif h > w * 1.15:
            orientations.append('portrait')
        else:
            orientations.append('square')
    return orientations


def fill_transparent_frames(
        base_rgba: Image.Image,
        patch_paths: list[str],
        target_width: int = -1,
        target_height: int = -1,
        reorder_by_orientation: bool = True,
        pad: int = 4,
    ) -> Image.Image:

    if base_rgba.mode != 'RGBA':
        raise ValueError("Base image must be in RGBA mode")

    start = time.time()
    print(start, "Starting fill_transparent_frames")
    if target_width > 0 and target_height <= 0:
        target_height = int(base_rgba.height * target_width / base_rgba.width + 0.5)
    elif target_height > 0 and target_width <= 0:
        target_width = int(base_rgba.width * target_height / base_rgba.height + 0.5)

    if target_width > 0:
        print(time.time() - start, f"Resizing base image to {target_width}x{target_height}")
        base_rgba = base_rgba.resize((target_width, target_height))


    transparent_regions = detect_transparent_regions(base_rgba)
    print(time.time() - start, "Transparent regions detected")
    print("Detected regions:", transparent_regions)
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


    composite = Image.new('RGBA', base_rgba.size)
    print(time.time() - start, "Base image converted to RGB for pasting patches")

    for region, patch_path in zip(transparent_regions, patch_paths):
        print(time.time() - start, f"Processing region with centroid {region['centroid']} and patch")   
        patch = Image.open(patch_path).convert('RGBA')
        patch_rs = patch.resize((region['width'] + pad, region['height'] + pad), Image.LANCZOS)

        # for squares, remove the nearest 90° chunk
        patch_rot = patch_rs.rotate(-region['angle'], expand=True)

        px = int(region['centroid']['x'] - patch_rot.width / 2)
        py = int(region['centroid']['y'] - patch_rot.height / 2)
        composite.paste(patch_rot.convert('RGB'), (px, py), patch_rot.split()[-1])

        print(time.time() - start, f"Patch pasted at ({px}, {py})")

    composite.paste(base_rgba, (0, 0), base_rgba.split()[-1])

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
    parser.add_argument('--pad' , type=int, default=4, help='Padding for the patches')
    args = parser.parse_args()

    result = fill_transparent_frames(args.base_img, args.patches, args.width, args.height, args.reorder, args.pad)
    if args.output:
        result.save(args.output)
    else:
        result.show()
