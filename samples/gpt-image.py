# This is a sample code to generate an image using OpenAI's gpt-image-1 model and a winding snippet.

import base64
from openai import OpenAI
from wind import snippet

def save_img(img, filename):
    image_bytes = base64.b64decode(img.data[0].b64_json)
    with open(filename, "wb") as f:
        f.write(image_bytes)


client = OpenAI()
#img = client.images.generate(model="gpt-image-1", prompt=snippet, n=1, size="1024x1024")
#save_img(img, "gpt-image-1-wind-snippet.png")

with open("wind_on_the_grass.md", "r") as f:
    snippet = f.read()
    img = client.images.generate(model="gpt-image-1", prompt=snippet, n=1, size="1536x1024", quality="high")
    save_img(img, "gpt-image-1-wind_on_the_grass.png")