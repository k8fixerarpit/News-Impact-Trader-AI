from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Boolean, Text
from sqlalchemy.sql import func
from .db import Base

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100))
    title = Column(Text)
    url = Column(String(1024))
    published_at = Column(DateTime)
    raw = Column(JSON)

class Impact(Base):
    __tablename__ = 'impacts'
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), index=True)
    score = Column(Float)
    reason = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), index=True)
    impact_id = Column(Integer)
    bias = Column(String(20))
    payload = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
