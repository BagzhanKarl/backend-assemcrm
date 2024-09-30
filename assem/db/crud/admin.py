# services/bagzhan_service.py
from sqlalchemy import and_
from sqlalchemy.orm import Session

from assem.db.models import Whatsapp
from assem.db.models.admin import Bagzhan
from assem.service.whapi.send_message import react_to_message_token


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

def check_meeting_on_date(chat_id: str, date: str, db: Session):
    meeting = db.query(Bagzhan).filter(Bagzhan.chat_id == chat_id, Bagzhan.date == date).first()
    if meeting:
        return True  # Встреча есть
    return False  # Встречи нет

def check_user_has_meeting(chat_id: str, db: Session):
    meeting = db.query(Bagzhan).filter(Bagzhan.chat_id == chat_id).first()
    if meeting:
        return True  # Есть запланированная встреча
    return False  # Запланированных встреч нет

def cancel_meeting(chat_id: str, date: str, db: Session):
    meeting = db.query(Bagzhan).filter(Bagzhan.chat_id == chat_id, Bagzhan.date == date).first()
    if meeting:
        db.delete(meeting)
        db.commit()
        return "Meeting successfully canceled."
    else:
        return "No meeting found on the given date."

def find_meetings_by_date(date: str, db: Session):
    meetings = db.query(Bagzhan).filter(Bagzhan.date == date).all()
    if meetings:
        return meetings  # Возвращаем список встреч на выбранную дату
    else:
        return []  # Встреч не найдено

def react_to_message(text: str, emoji: str, chat_id: str, db: Session):
    messages = db.query(Whatsapp).filter(and_(Whatsapp.text_body == text, Whatsapp.chat_id == chat_id)).first()

    react_to_message_token('THjJOt2vo26nYYj4IbqKXVqInFv1wx55', messages.id, emoji)

    return 'Вы реагировали на сообщение пользователя с эмодзи'

