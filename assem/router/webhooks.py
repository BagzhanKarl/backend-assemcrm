# router/webhooks.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from assem.db.database import get_db
from assem.models import Whatsapp
from assem.schemas import WebhookRequest, MessageBody

webhook_router = APIRouter(prefix='/api/v2/webhook', tags=['Webhook'])

@webhook_router.post('/whatsapp')
async def handle_whatsapp_webhook(request: WebhookRequest, db: Session = Depends(get_db)):
    for msg in request.messages:
        message = Whatsapp(
            message_id=msg.id,
            chat_id=msg.chat_id,
            sender_name=msg.from_name,
            message_type=msg.type,
            timestamp=msg.timestamp,
            text_body=msg.text['body'],  # Предполагаем, что текст сообщения хранится в поле 'body'
            channel_id=request.channel_id,
            status=0,
        )
        db.add(message)
    db.commit()
    return {"detail": "Messages saved successfully"}
