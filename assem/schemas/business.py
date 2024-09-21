# schemas/business.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CreateBusiness(BaseModel):
    title: str
    branch: int = 1
    user_role: int = 0
