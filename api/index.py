from flask import Flask, request, jsonify
import requests
from PIL import Image

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "OCR API working",
        "endpoint": "/ocr"
    })

@app.route("/ocr", methods=["POST"])
def ocr():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    language = request.form.get("language", "ara")

    file = request.files["image"]

    path = "/tmp/m.png"
    file.save(path)

    img = Image.open(path)
    img = img.resize((800, 800))

    small_path = "/tmp/small.jpg"
    img.save(small_path, quality=40)

    url = "https://api.ocr.space/parse/image"

    payload = {
        "apikey": "helloworld",
        "language": language
    }

    with open(small_path, "rb") as f:
        r = requests.post(url, files={"file": f}, data=payload)

    data = r.json()

    if "ParsedResults" in data:
        text = data["ParsedResults"][0]["ParsedText"]
        return jsonify({
            "language": language,
            "text": text
        })
    else:
        return jsonify(data)
