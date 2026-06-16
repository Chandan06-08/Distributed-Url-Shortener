from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.database import get_db
from app.models import URL
from app.schemas import URLRequest
from fastapi import Depends
from sqlalchemy.orm import Session
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
def shorten_url(
    request: URLRequest,
    db: Session = Depends(get_db)
):
    while True:
        code = generate_code()

        existing_url = db.query(URL).filter(
            URL.short_code == code
        ).first()

        if existing_url is None:
            break

    new_url = URL(
        short_code=code,
        original_url=request.url
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "short_code": code
    }

@app.get("/{code}")
def redirect_to_url(
    code: str,
    db: Session = Depends(get_db)
):
    url_record = db.query(URL).filter(
        URL.short_code == code
    ).first()

    if url_record is None:
        raise HTTPException(
            status_code=404,
            detail="Short code not found"
        )

    return RedirectResponse(
        url=url_record.original_url
    )