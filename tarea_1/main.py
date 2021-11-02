from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/news/", response_model= schemas.New)
def create_new(new: schemas.NewCreate, db: Session = Depends(get_db)):
    db_new = crud.get_new_by_id(db, id =new.id)
    if db_new:
        raise HTTPException(status_code=400, detail="No existe noticia con ese id")
    return crud.create_new(db=db, new=new)





@app.get("/news/{new_id}", response_model=schemas.New)
def read_new(new_id: int, db: Session = Depends(get_db)):
    db_new = crud.get_new(db, new_id=new_id)
    if db_new is None:
        raise HTTPException(status_code=404, detail="New not found")
    return db_new

