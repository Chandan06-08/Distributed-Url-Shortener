from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class URL(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    short_code = Column(String(10), unique=True, nullable=False)
    original_url = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    click_count = Column(BigInteger, nullable=False, default=0)
    expires_at = Column(DateTime, nullable=True)


   
