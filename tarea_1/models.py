from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base_tarea

class New (Base_tarea):

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), unique=True, index = True)
    date = Column(String(10)) 
    url = Column(String(50))
    media_outlet = Column(String(20))

    has_category = relationship("Has_category", back_populates = "pertenece")

class Has_category (Base_tarea):

    __tablename__ = "has_category"

    value = Column(String())

    value_id = Column(Integer, ForeignKey(news.id))

    pertenece = relationship("New", back_populates = "has_category")
