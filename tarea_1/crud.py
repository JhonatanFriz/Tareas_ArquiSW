from sqlalchemy.orm import Session

from . import models, schemas

def get_new(db: Session, new_id):
    return db.query(models.New).filter(models.New.id == new_id).all()

def create_new(db: Session, new: schemas.NewCreate):
    db_new = models.New(**item.dict(), value_id = new_id
    db.add(db_new)
    db.commit()
    db.refresh(db_new)
    return db_new
