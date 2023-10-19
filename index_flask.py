import json
import os
import re

from flask import Flask, Response, jsonify, render_template, send_file

app = Flask(__name__, template_folder="public", static_folder="public")

status_codes = {}
with open("db.json", encoding="utf-8") as f:
    status_codes = json.load(f)

@app.route("/")
def home():
    """
    Home.
    """
    return render_template('index.html')

@app.route("/favicon.<ext>")
def favicon(ext):
    """
    favicon.ico
    """
    print(f'favicon.{ext}')
    return send_file("public/favicon.ico")

@app.get("/favicon-<size>.png")
def faviconpng(size):
    """
    favicon-{size}.png
    """
    return send_file(f"public/favicon-{size}.png")


# Route to get all status codes
@app.route("/codes")
def get_codes():
    """
    Get all status codes.
    """
    return jsonify(status_codes)

@app.route("/<int:code>")
def get_status(code):
    """
    Get status code by code.
    """
    code = str(code)

    if not re.match(r"\d{3}$", code):
        return Response("Not Acceptable", status=406, content_type="text/plain")

    if code not in status_codes:
        return Response("Not Implemented", status=501, content_type="text/plain")

    content = status_codes[code]["code"]
    return Response(content, status=int(code), content_type="text/plain")


@app.route("/<any>/<path>")
async def invalid_code():
    """
    Invalid code.
    """
    return Response("Bad Request", status=400, content_type="text/plain")

if __name__ == "__main__":
    PORT = os.getenv("PORT", "8080")
    HOST = os.getenv("HOST", "0.0.0.0")
    app.run(host=HOST, port=int(PORT))
