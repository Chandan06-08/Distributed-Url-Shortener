from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import URL
from app.schemas import URLRequest
from app.cache import redis_client
from datetime import datetime, timedelta

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
    expires_at = None

    if request.expires_in_days is not None:
        expires_at = datetime.now() + timedelta(days=request.expires_in_days)

    new_url = URL(
        short_code=code,
        original_url=request.url,
        expires_at=expires_at
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
    cached_url = redis_client.get(code)

    if cached_url:
        print("CACHE HIT")

        url_record = db.query(URL).filter(
            URL.short_code == code
        ).first()

        if url_record:
            url_record.click_count += 1
            db.commit()

        return RedirectResponse(url=cached_url)

    print("CACHE MISS")

    url_record = db.query(URL).filter(
        URL.short_code == code
    ).first()
    if url_record.expires_at is not None:
        if datetime.now() >= url_record.expires_at:
            raise HTTPException(
                status_code=410,
                detail="This URL has expired"
            )

    if url_record is None:
        raise HTTPException(
            status_code=404,
            detail="Short code not found"
        )

    redis_client.set(
        code,
        url_record.original_url
    )

    url_record.click_count += 1
    db.commit()

    return RedirectResponse(
        url=url_record.original_url
    )