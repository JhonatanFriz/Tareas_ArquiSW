from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base

class News(Base):

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    date = Column(Date) 
    url = Column(String(180), unique=True)
    media_outlet = Column(String(25))
    category = Column(String(15))

class HasCategory(Base):
    __tablename__ = 'has_category'

    value = Column(String(15), primary_key=True, index=True)