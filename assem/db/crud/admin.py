# services/bagzhan_service.py

from sqlalchemy.orm import Session
from assem.db.models.admin import Bagzhan

def save_bagzhan(chat_id: str, date: str, note: str, db: Session):
    bagzhan = Bagzhan(
        chat_id=chat_id,
        date=date,
        note=note,
        is_completed=False
    )
    db.add(bagzhan)
    db.commit()
    db.refresh(bagzhan)
    return "Meeting scheduled successfully."
