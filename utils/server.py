from flask import Flask, Response
from PIL import Image
from epd_image_processor import convert_image_to_list_of_bytes

frames = convert_image_to_list_of_bytes(
    Image.open("test_image.png"),
    (768, 960),
    2
)


app = Flask(__name__)


@app.route("/")
def index():
    payload = frames[0]
    return Response(payload, mimetype="application/octet-stream")
