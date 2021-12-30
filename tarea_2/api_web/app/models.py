from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import ast

from .database import Base

class News(Base):

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(), unique=False, index=False)
    date = Column(Date, unique=False, index=True) 
    url = Column(String(), unique=False, index=False)
    media_outlet = Column(String(), unique=False, index=False)
    category = Column(String(), unique=False, index=False)