# router/branch.py
from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from assem.db.database import get_db
from assem.db.models import Messages, AiSettings, Bagzhan
from assem.db.schemas import ChatArray, Chat, SystemSettings
from openai import OpenAI
from assem.security.send_message import send_message
from assem.service.openai import chat_with_ai

api_key = ""
client = OpenAI(api_key=api_key)

ai = APIRouter(prefix='/api/v2/ai', tags=['ИИ'])


@ai.get('/{platform}/{chatid}', response_model=ChatArray)
async def get_chat_messages(platform: str, chatid: str, db: Session = Depends(get_db)):
    ai_settings = db.query(AiSettings).filter(AiSettings.platform == platform).all()

    if not ai_settings:
        raise HTTPException(status_code=404, detail="System settings not found")


    messages = db.query(Messages).filter(Messages.chat_id == chatid).all()

    if not messages:
        raise HTTPException(status_code=404, detail="Messages not found")

    chat_messages = [
        Chat(
            role=setting.role,
            content=setting.content
        )
        for setting in ai_settings
    ] + [
        Chat(
            role="user" if message.side == "in" else "assistant",
            content=message.text
        )
        for message in messages
    ]

    return ChatArray(messages=chat_messages)
@ai.post('/system/settings/{platform}')
async def create_system_messages(platform: str, content: SystemSettings, db: Session = Depends(get_db)):
    settings = AiSettings(platform=platform, role="system", content=content.content)

    db.add(settings)
    db.commit()
    db.refresh(settings)

    return [settings]
@ai.post('/system/settings/get/{platform}')
async def get_all_system_messages(platform: str, db: Session = Depends(get_db)):
    settings = db.query(AiSettings).filter(AiSettings.platform == platform).all()
    return settings
@ai.delete('/system/settings/{id}', status_code=204)
async def delete_system_message(id: int, db: Session = Depends(get_db)):
    # Находим запись по id
    settings = db.query(AiSettings).filter(AiSettings.id == id).first()

    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")

    # Удаляем запись
    db.delete(settings)
    db.commit()

    return {"detail": "Settings deleted successfully"}
@ai.put('/system/settings/{id}')
async def update_system_message(id: int, content: SystemSettings, db: Session = Depends(get_db)):
    # Находим запись по id
    settings = db.query(AiSettings).filter(AiSettings.id == id).first()

    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")

    # Обновляем запись
    settings.content = content.content
    db.commit()
    db.refresh(settings)

    return settings
@ai.post('/generate/{platform}/{chatid}')
async def generate_answer_ai(platform: str, chatid: str, db: Session = Depends(get_db)):
    try:
        response = chat_with_ai(platform, chatid, db)
        # Отправляем сообщение пользователю (если необходимо)
        send = send_message('7GKIxS6r8CC9OdwE62RtQmwfscqfBiLn', 0, chatid, response[0])

        return {"response": response, 'status': send}
    except HTTPException as e:
        return {"detail": e.detail}

@ai.get('/bagzhan')
async def get_all_bagzhan_records(db: Session = Depends(get_db)):
    records = db.query(Bagzhan).all()
    if not records:
        raise HTTPException(status_code=404, detail="No records found")
    return records
