
def outpaint(image_path, left, right, up, down):
    """
    Outpaint a thin border around an image, to fill bleed areas

    This function:
     1. resizes the image to create a border around it
     2. puts the original image in the center of the new image
     3. applies a Gaussian blur to the border

    The resize is done in layers, with each layer being 7 pixels smaller than the previous one.

    This results in a slightly better image than a simple mirror at the edges.
    """

    # TODO: this implementation only supports padding on all sides
    # should be easy to extend to support different padding on each side


    # Load the original image (H×W×C)
    img = Image.open('001.png').convert('RGB')
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
    out_img.save('outpaint-resize.png')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Outpaint a thin border around an image, to fill bleed areas")
    parser.add_argument('img', type=str, help='Path to the original image')
    parser.add_argument('--output', type=str, help='Path to save the output image')
    parser.add_argument('--left', type=int, default=0, help='Padding size, left side, pixels')
    parser.add_argument('--right', type=int, default=0, help='Padding size, right side, pixels')
    parser.add_argument('--up', type=int, default=0, help='Padding size, top side, pixels')
    parser.add_argument('--down', type=int, default=0, help='Padding size, bottom side, pixels')
    args = parser.parse_args()

    result = outpaint(args.img, args.left, args.right, args.up, args.down)
    if args.output:
        result.save(args.output)
    else:
        result.show()
