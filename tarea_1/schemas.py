from typing import List, Optional

from pydantic import BaseModel

class NewBase(BaseModel):
    title: str
    date: str
    url: str
    media_outlet: str

class NewCreate(NewBase):
    pass

class New(NewBase):
    id: int
    value_id: int

    class Config:
        orm_mode = True



class CategoryBase(BaseModel):
    value: str

class Has_category(CategoryBase):

    has_category: List[New] = []

    class Config:
        orm_mode = True
