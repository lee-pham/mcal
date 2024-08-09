from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def index():
    text = (("a" * 46079) + "e") * 1
    return Response(text, mimetype="application/octet-stream")
