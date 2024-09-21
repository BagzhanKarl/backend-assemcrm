# api_routers/user.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session

from assem.schemas import UserCreate, ResponseUserCreate, UserLogin
from assem.db.database import engine, get_db, Base
from assem.models import User
from assem.security import hash_password, generate_token, verify_password, decode_token

User.metadata.create_all(bind=engine)

user_router = APIRouter(prefix='/api/v1/public/users', tags=['Пользователи'])

@user_router.post('/registration', response_model=ResponseUserCreate)
async def create_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == user.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким телефоном уже существует")

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        hashed_password=hash_password(user.password),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        role_id=None,
        business_id=None  # Изначально бизнес не указан
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = generate_token(new_user.id)

    response.set_cookie(key="access_token", value=token, httponly=True, max_age=3600)
    answere = {'status': True, "api": "v1", "data": [new_user]}
    return answere

@user_router.post("/login")
async def login_user(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.phone == user.phone).first()
    if existing_user == None:
        raise HTTPException(status_code=400, detail="Неправильный номер телефона или пароль")

    passChek = verify_password(user.password, existing_user.hashed_password)

    if(passChek == False):
        raise HTTPException(status_code=400, detail="Неправильный номер телефона или пароль")

    token = generate_token(existing_user.id)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=3600)
    return {'phone': user.phone, 'password': existing_user.hashed_password}


@user_router.get('/check_authorization')
async def check_authorization(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authorized")

    payload = decode_token(access_token)
    return {
        "message": "Пользователь авторизован",
        "user_id": payload.get("user")
    }

@user_router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="access_token")  # Удаляем токен из cookies
    return {"status": True, "message": "Successfully logged out"}
