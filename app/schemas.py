from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str
    expires_in_days: int | None = None