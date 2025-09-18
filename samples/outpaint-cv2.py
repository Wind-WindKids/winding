import cv2
import numpy as np

# 1. load your image
img = cv2.imread("001.png")
h, w = img.shape[:2]

# 2. choose your outpaint width (e.g. 21 px)
pad = 21

# 3. make a new blank canvas: same height, wider
canvas = np.zeros((h + 2 * pad, w + 2 * pad, 3), dtype=img.dtype)
canvas[pad:pad+h, pad:w + pad] = img

# 4. build the mask: 255 where we want inpainting
mask = np.zeros((h + 2 * pad, w + 2 * pad), dtype=np.uint8)
mask[:, :pad] = 255
mask[:, w + pad:] = 255
mask[:pad, :] = 255
mask[h + pad:, :] = 255

# 5. inpaint (you can also try cv2.INPAINT_NS)
out = cv2.inpaint(canvas, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

cv2.imwrite("001-outpainted.png", out)
