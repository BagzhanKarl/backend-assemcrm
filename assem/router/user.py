from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from assem.db.database import engine, get_db, Base
from assem.models import User
from assem.security import hash_password, generate_token, verify_password, decode_token

User.metadata.create_all(bind=engine)

user_router = APIRouter(prefix='/api/v1/public/users', tags=['Пользователи'])

@user_router.post('/registration')
async def registration(id: str):
    return id