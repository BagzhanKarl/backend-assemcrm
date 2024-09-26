# router/webhooks.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from assem.db.database import get_db
from assem.models import Whatsapp, Messages
from assem.schemas import WebhookRequest, MessageBody

webhook_router = APIRouter(prefix='/api/v2/webhook', tags=['Webhook'])

@webhook_router.post('/whatsapp')
async def handle_whatsapp_webhook(platform: str, request: WebhookRequest, db: Session = Depends(get_db)):
    for msg in request.messages:
        message = Whatsapp(
            message_id=msg.id,
            chat_id=msg.chat_id,
            sender_name=msg.from_name,
            message_type=msg.type,
            timestamp=msg.timestamp,
            text_body=msg.text['body'],  # Предполагаем, что текст сообщения хранится в поле 'body'
            channel_id=request.channel_id,
            business=platform,
            status=0,
        )
        messages = Messages(
            business=platform,
            chat_id=msg.chat_id,
            text=msg.text['body'],
            read=False,
            side="in",
        )
        db.add(message)
        db.add(messages)
    db.commit()
    return {"detail": "Messages saved successfully"}

@webhook_router.get('/whatsapp/all')
async def get_all(db: Session = Depends(get_db)):
    messages = db.query(Whatsapp).all()
    return messages