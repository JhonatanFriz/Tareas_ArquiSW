from sqlalchemy.orm import Session

from . import models, schemas

def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.News).offset(skip).limit(limit).all()
