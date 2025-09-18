import requests, os
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/edit/outpaint",
    headers={
        "authorization": f"Bearer " + STABILITY_API_KEY,
        "accept": "image/*"
    },
    files={
        "image": open("001.png", "rb")
    },
    data={
        "left": 32,
        "up": 32,
        "down": 32,
        "output_format": "png",
        "creativity": 0.1,
        "prompt": "An image with soft blurred edges",
    },
)

if response.status_code == 200:
    with open("./001-debleed.png", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(str(response.json()))