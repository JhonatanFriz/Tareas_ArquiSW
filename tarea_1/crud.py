from sqlalchemy.orm import Session

from . import models, schemas

#Para obtener las noticias
def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.News).offset(skip).limit(limit).all()

#Para obtener una noticia en especifico
def get_new(db: Session, new_id: int):
    return db.query(models.News).filter(models.News.id == new_id).first()