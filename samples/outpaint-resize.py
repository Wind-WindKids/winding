from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter

def outpaint(filename, pad = 21):
    # Load the original image (H×W×C)
    img = Image.open(filename).convert('RGB')
    img_arr = np.array(img)
    h, w = img_arr.shape[:2]

    # Padding and layers
    pad = 21
    layers = list(range(pad, 0, -7))
    print(f"Layers: {list(layers)}")

    # Create blank canvas
    canvas = np.zeros((h + 2 * pad, w + 2 * pad, 3), dtype=np.uint8)

    # Overlay resized layers
    for ipad in layers:
        new_h, new_w = h + 2 * ipad, w + 2 * ipad
        resized = img.resize((new_w, new_h), resample=Image.LANCZOS)
        resized_arr = np.array(resized)
        y0 = pad - ipad
        x0 = pad - ipad
        canvas[y0:y0 + new_h, x0:x0 + new_w] = resized_arr

    # Create mask for border region plus a couple pixels inside (True = blur)
    mask = np.ones((h + 2 * pad, w + 2 * pad), dtype=bool)
    # Exclude central area minus 2px inside border
    inner_top = pad + 1
    inner_left = pad + 1
    inner_bottom = pad + h - 1
    inner_right = pad + w - 1
    mask[inner_top:inner_bottom, inner_left:inner_right] = False

    # Apply Gaussian blur to entire canvas
    sigma = 3  # blur radius
    blurred = np.zeros_like(canvas, dtype=np.float32)
    for c in range(3):
        blurred[..., c] = gaussian_filter(canvas[..., c].astype(np.float32), sigma=sigma)

    # Composite: use blurred where mask True, keep original where False
    final = canvas.astype(np.float32)
    for c in range(3):
        ch = final[..., c]
        ch[mask] = blurred[..., c][mask]
        final[..., c] = ch

    final_uint8 = np.clip(final, 0, 255).astype(np.uint8)
    # Save the final image
    out_img = Image.fromarray(final_uint8)
    out_img.save(filename)

def main():
    import sys
    if sys.argv[1] != "--targets":
        print("Usage: outpaint-resize.py --targets <filename.png> [filename.png] ...")
    else:
        for f in sys.argv[2:]:
            print(f"Outpainting {f}")
            outpaint(f)



if __name__ == "__main__":
    main()
