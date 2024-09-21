from pydantic import BaseModel
from typing import Optional, List

class CreateCategory(BaseModel):
    title: str
    admin: str

class CreateRole(BaseModel):
    title: str
    admin: str

class CreateType(BaseModel):
    category_id: int
    title: str
    admin: str