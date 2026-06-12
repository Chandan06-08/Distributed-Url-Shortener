from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from app.models import URLRequest
from app.storage import url_store
import random
import string

app = FastAPI()



def generate_code(length=6):
    chars = string.ascii_letters + string.digits

    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )


@app.post("/shorten")
def shorten_url(request: URLRequest):
    while True:
        code = generate_code()
        if code not in url_store:
            break

    url_store[code] = request.url

    return {
        "short_code": code
    }

@app.get("/{code}")
def redirect_to_url(code: str):
    if code not in url_store:
        raise HTTPException(status_code=404, detail="Short code not found")
    original_url = url_store[code]
    return RedirectResponse(url=original_url)