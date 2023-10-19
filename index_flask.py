import json
import os
import re

from flask import Flask, jsonify, make_response, render_template, send_file

app = Flask(__name__, template_folder="public", static_folder="public")

status_codes = {}
with open("db.json", encoding="utf-8") as f:
    status_codes = json.load(f)


def custom_make_response(content: str, code: int):
    """
    Custom make response.
    """
    response = make_response(jsonify(content), code)
    response.headers['Cache-Control'] = 'public, max-age=604800, immutable'
    return response

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


@app.route("/codes")
def get_codes():
    """
    Get all status codes.
    """
    return custom_make_response(status_codes, 200)

@app.route("/<int:code>")
def get_status(code):
    """
    Get status code by code.
    """
    code = str(code)

    if not re.match(r"\d{3}$", code):
        return custom_make_response("Not Acceptable", 406)

    if code not in status_codes:
        return custom_make_response("Not Implemented", 501)

    content = status_codes[code]["code"]
    return custom_make_response(content, int(code))


@app.route("/<_any>/<_path>")
def invalid_code(_any, _path):
    """
    Invalid code.
    """
    return custom_make_response("Bad Request", 400)

if __name__ == "__main__":
    PORT = os.getenv("PORT", "8080")
    HOST = os.getenv("HOST", "0.0.0.0")
    app.run(host=HOST, port=int(PORT))
