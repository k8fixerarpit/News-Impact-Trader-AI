from sqlalchemy import Column, Integer, String, DateTime
from backend.db import Base

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    source = Column(String)
    ticker = Column(String)
    published_at = Column(DateTime)
