import json
import os
import re

from flask import Flask, Response, jsonify, render_template

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

@app.route("/favicon.ico")
def favicon():
    """
    Favicon.
    """
    return app.send_static_file("public/favicon.ico")

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
    app.run(host="0.0.0.0", port=int(PORT))
