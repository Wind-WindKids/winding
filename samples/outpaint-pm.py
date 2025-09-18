# PatchMatch outpainting on all four sides by 21 px
# Requires: pip install pypatchmatch pillow opencv-python numpy

import numpy as np
from PIL import Image
import cv2
from patchmatch import inpaint

# 1. Load and convert to numpy array
img = np.array(Image.open("001.png").convert("RGB"))
h, w = img.shape[:2]
pad = 21  # pixels to extend on each side

# 2. Create a canvas with a border
canvas = np.zeros((h + 2*pad, w + 2*pad, 3), dtype=img.dtype)
canvas[pad:pad+h, pad:pad+w] = img

# 3. Build the mask (255 = hole)
mask = np.zeros((h + 2*pad, w + 2*pad), dtype=np.uint8)
mask[:pad, :]     = 255  # top
mask[h+pad:, :]   = 255  # bottom
mask[:, :pad]     = 255  # left
mask[:, w+pad:]   = 255  # right

# 4. PatchMatch inpainting
#    patch_size: size of square patches (try 7 or 9)
#    num_iter: number of PatchMatch iterations (5–10 is typical)
filled = inpaint(canvas, mask, patch_size=7, num_iter=7)

# 5. Poisson blend for seamless result
center = (pad + w//2, pad + h//2)
seamless = cv2.seamlessClone(filled, canvas, mask, center, cv2.NORMAL_CLONE)

# 6. Save the outpainted image
output = Image.fromarray(seamless)
output.save("outpaint_patchmatch_all_sides.png")

