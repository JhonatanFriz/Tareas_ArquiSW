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

@app.get("/news/", response_model=List[schemas.News])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    news = crud.get_news(db, skip=skip, limit=limit)
    return news
