from sqlalchemy.orm import Session
from sqlalchemy import and_

from . import models, schemas

#Para obtener por fechas
def get_news(db: Session, from_: str = '2021-10-20', to_: str = '2022-10-21', limit: int = 100):
    return db.query(models.News).filter(and_(models.News.date >= from_, models.News.date < to_)).limit(limit).all()

#Para obtener las noticias
#def get_news(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.News).offset(skip).limit(limit).all()

#Para obtener una noticia en especifico
#def get_new(db: Session, new_id: int):
#    return db.query(models.News).filter(models.News.id == new_id).first()
