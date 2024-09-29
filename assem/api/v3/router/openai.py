# router/role.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from assem.db.database import get_db
from assem.db.models import GTPOpen
from assem.db.schemas.role import GPTAdd

openai_router = APIRouter(prefix="/api/admin/openai/token", tags=["OpenAI"])

# Добавление новой роли
@openai_router.post("/add")
def add_token(role: GPTAdd, db: Session = Depends(get_db)):
    db_role = GTPOpen(token=role.token, admin=role.admin)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

