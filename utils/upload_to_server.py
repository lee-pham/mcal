import requests
import sys
import zlib
from epd_image_processor import convert_image_to_list_of_bytes
from PIL import Image

url = "http://picow.local/"


payload = convert_image_to_list_of_bytes(
    Image.open("test_image.png"),
    (768, 960),
    2
)[0].hex()



headers = {
    "User-Agent": "framework/upload_to_server.py",
    "Content-Type": "application/octet-stream",
    # Content-Length is calculated and included by the requests library
}

response = requests.request(
    "PUT",
    url,
    data=payload,
    headers=headers
)
print(response.text)
