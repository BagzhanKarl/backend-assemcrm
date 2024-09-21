from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from assem.db.database import engine, get_db, Base
from assem.schemas.system_settings import CreateCategory, CreateRole, CreateType
from assem.models.system import Category, Role, Type

system_router = APIRouter(prefix='/api/v1/public/system', tags=['Системные настройки'])

@system_router.post('/category')
async def create_category(category: CreateCategory, db: Session = Depends(get_db)):
    if(category.admin != 'baxamk12345678'):
        raise HTTPException(status_code=400, detail="Не правильный код админстратора")

    new_category = Category(
        title=category.title,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category;

@system_router.post('/role')
async def create_role(role: CreateRole, db: Session = Depends(get_db)):
    if(role.admin != 'baxamk12345678'):
        raise HTTPException(status_code=400, detail="Не правильный код админстратора")

    new_role = Role(
        name=role.title,
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role;

@system_router.post('/type')
async def create_type(type: CreateType, db: Session = Depends(get_db)):
    if(type.admin != 'baxamk12345678'):
        raise HTTPException(status_code=400, detail="Не правильный код админстратора")
    category = db.query(Category).filter(Category.id == type.category_id).first()
    if category == False:
        raise HTTPException(status_code=400, detail="Категория не найдено")

    new_type = Type(
        title=type.title,
        category_id=category.id
    )
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type

@system_router.get('/category/list')
async def get_category_list(db: Session = Depends(get_db)):
    category = db.query(Category).all()
    answere = {'status': True, 'api': 'v1', 'data': [category]}

    return answere

@system_router.get('/roles/list')
async def get_roles_list(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    answere = {'status': True, 'api': 'v1', 'data': [roles]}

    return answere

@system_router.get('/types/{category_id}')
async def get_types_on_category(category_id: int, db: Session = Depends(get_db)):
    types = db.query(Type).filter(Type.category_id == category_id).all()
    category = db.query(Category).filter(Category.id == category_id).first()
    answere = {'status': True, 'api': 'v1', 'category': category.title, 'data': [types]}
    return answere
