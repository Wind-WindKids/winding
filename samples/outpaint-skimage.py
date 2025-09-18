import numpy as np
from skimage import io, img_as_float, img_as_ubyte
from skimage.restoration import inpaint_biharmonic

# 1. Load your image (H×W×C) as uint8
img = io.imread("001.png")
h, w = img.shape[:2]

# 2. How many pixels to pad on each side?
pad = 21

# 3. Make a float canvas in [0,1]
canvas = np.zeros((h + 2*pad, w + 2*pad, img.shape[2]), dtype=np.float32)
canvas[pad:pad+h, pad:pad+w] = img_as_float(img)

# 4. Boolean mask of the padded border
mask = np.zeros((h + 2*pad, w + 2*pad), dtype=bool)
mask[:pad, :]     = True   # top
mask[h+pad:, :]   = True   # bottom
mask[:, :pad]     = True   # left
mask[:, w+pad:]   = True   # right

# 5. Inpaint on the float canvas
#    - If your skimage ≥0.19: use `channel_axis=-1`
#    - If your skimage ≤0.18: use `multichannel=True` instead
filled = inpaint_biharmonic(
    canvas,
    mask,
    channel_axis=-1
)

# 6. Convert back to uint8 and save
out = img_as_ubyte(np.clip(filled, 0.0, 1.0))
io.imsave("outpaint_skimage_fixed.png", out)
