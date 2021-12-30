from typing import Dict, Any, Type
from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel, Field

class News(BaseModel):
    id: int
    title: str
    date: date
    url: str
    media_outlet: str
    category: str

    class Config:
        orm_mode = True
        allow_mutation = True