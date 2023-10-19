import json
import os
import re

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="HTTP Status Codes", redoc_url=None)

status_codes = {}
with open("db.json", encoding="utf-8") as f:
    status_codes = json.load(f)


@app.get("/", include_in_schema=False)
async def root():
    """
    Root.
    """
    return FileResponse("public/index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Favicon.
    """
    return FileResponse("public/favicon.ico")


@app.get("/codes", summary="Get all status codes.")
async def get_codes():
    """
    Get all status codes.
    """
    return status_codes


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
        return JSONResponse(
            content="Not Acceptable", status_code=status.HTTP_406_NOT_ACCEPTABLE
        )

    if code not in status_codes:
        return JSONResponse(
            content="Not Implemented", status_code=status.HTTP_501_NOT_IMPLEMENTED
        )

    content = status_codes[code]["code"]
    return JSONResponse(content=content, status_code=int(code))


@app.get("/{any}/{path}", include_in_schema=False)
async def invalid_code():
    """
    Invalid code.
    """
    return JSONResponse(content="Bad Request", status_code=status.HTTP_400_BAD_REQUEST)


if __name__ == "__main__":
    PORT = os.getenv("PORT", "8080")
    uvicorn.run(app, port=int(PORT))
