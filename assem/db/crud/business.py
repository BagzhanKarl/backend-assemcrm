from fastapi import Depends
from sqlalchemy.orm import Session

from assem.db.database import get_db
from assem.db.models import Business


async def add_token(token: str, business: int, db: Session = Depends(get_db)):
    update_business = db.query(Business).filter(Business.id == business).first()

    update_business.whapi_token = token

    db.add(update_business)
    db.commit()
    db.refresh(update_business)
    return update_business