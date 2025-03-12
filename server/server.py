from flask import Flask, Response

app = Flask(__name__)

@app.route("/data")
def index():
    text = (("a" * 46080*2) + "e") * 1
    # text = "HELO worldddd".encode()
    # response = Response(text, mimetype="application/octet-stream")
    binary_data = bytes([0x01, 0x02, 0x03, 0x04, 0x00, 0x05, 0x06, 0x07, 0x08])
    # Send the raw binary data directly in the response
    return Response(text, content_type='application/octet-stream')

app.run(host="0.0.0.0",
        port=5000,
        debug=True)
