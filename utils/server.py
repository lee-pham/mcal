from flask import Flask, Response
from PIL import Image
from epd_image_processor import convert_image_to_list_of_bytes

frames = convert_image_to_list_of_bytes(
    Image.open("test_image.png"),
    (768, 960),
    2
)

app = Flask(__name__)


@app.route("/0")
def handle0():
    text = frames[0].hex()
    return Response(text, mimetype="text/plain")


@app.route("/1")
def handle1():
    text = frames[1].hex()
    return Response(text, mimetype="text/plain")


@app.route("/2")
def handle2():
    text = frames[0].hex()
    return Response(text, mimetype="text/plain")


@app.route("/3")
def handle3():
    text = frames[1].hex()
    print("last frame sent")
    return Response(text, mimetype="text/plain")
