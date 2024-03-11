import requests
from PIL import Image
from epd_image_processor import convert_image_to_list_of_bytes


files = {
    "file": convert_image_to_list_of_bytes(Image.open("../render/calendar.png"), (768, 960), 2)[0]
}

r = requests.post(
    "http://picow.local",
    files=files
    )
print(r.text)
