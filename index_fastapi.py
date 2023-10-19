import json
import os
import re

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="HTTP Status Codes", redoc_url=None)
app.mount("/static", StaticFiles(directory="public"), name="static")

status_codes = {}
with open("db.json", encoding="utf-8") as f:
    status_codes = json.load(f)


def custom_make_response(content: str, code: int):
    """
    Custom make response.
    """
    return JSONResponse(
        content=content, status_code=code,
        headers={"Cache-Control": "public, max-age=604800, immutable"}
    )

@app.get("/", include_in_schema=False)
async def home():
    """
    Root.
    """
    with open("public/index.html", "r", encoding="utf-8") as content:
        content = content.read()
    return HTMLResponse(
        content,
        headers={
            "Cache-Control": "no-cache", 
            "Content-Type": "text/html",
        }
    )

@app.get("/favicon.{ext}", include_in_schema=False, response_class=HTMLResponse)
async def favicon(ext: str):
    """
    favicon.ico
    """
    print(f'favicon.{ext}')
    return FileResponse("public/favicon.ico")

@app.get("/favicon-{size}.png", include_in_schema=False, response_class=HTMLResponse)
async def faviconpng(size: str):
    """
    favicon-{size}.png
    """
    return FileResponse(f"public/favicon-{size}.png")


@app.get("/codes", summary="Get all status codes.")
async def get_codes():
    """
    Get all status codes.
    """
    return custom_make_response(status_codes, 200)


class StatusCode(BaseModel):
    """ 
    Status code model.
    """
    code: int

@app.get("/{code}", response_model=StatusCode, summary="Get a status code.")
async def get_status(code: int):
    """
    Get status code by code.
    """
    code = str(code)

    if not re.match(r"\d{3}$", code):
        return custom_make_response("Not Acceptable", code=status.HTTP_406_NOT_ACCEPTABLE)

    if code not in status_codes:
        return custom_make_response(
            "Not Implemented", code=status.HTTP_501_NOT_IMPLEMENTED
        )

    content = status_codes[code]["code"]
    return custom_make_response(content, code=int(code))


@app.get("/{any}/{path}", include_in_schema=False)
async def invalid_code():
    """
    Invalid code.
    """
    return custom_make_response("Bad Request", code=status.HTTP_400_BAD_REQUEST)


if __name__ == "__main__":
    PORT = os.getenv("PORT", "8080")
    HOST = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=HOST, port=int(PORT))
