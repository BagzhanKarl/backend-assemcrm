# api_routers/business.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session

from assem.db.database import get_db
from assem.models import User, Business
from assem.schemas.business import CreateBusiness
from assem.security import decode_token, generate_id

business_router = APIRouter(prefix='/api/v1/public/business', tags=['Бизнес'])


@business_router.post('/create/')
async def create_business(business: CreateBusiness, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    try:
        payload = decode_token(access_token)  # Используйте access_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    userid = payload.get('user')
    user = db.query(User).filter(User.id == userid).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_business = Business(
        title=business.title,
        branches=business.branch,
        platform=generate_id(),
        payment_link=None,
        thanks_link=None,
        is_active=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    user.business_id = new_business.id
    user.role_id = business.user_role
    db.commit()  # Сохраняем изменения в базе данных

    return {"user": [user], "business": [new_business]}


@business_router.get('/{business_id}/')
async def get_info(business_id: int, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    return {"business": business}

@business_router.get('/ai/{business_id}/')
async def get_info(business_id: int, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()

    return {"business": business}
