# services/ai_service.py

import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from assem.db.models import AiSettings, GTPOpen
from assem.db.models import Messages

from openai import OpenAI
from datetime import datetime

def chat_with_ai(platform: str, chat_id: str,  db: Session):
    api_key = db.query(GTPOpen).filter(GTPOpen.admin == 'assemteam').first()
    client = OpenAI(api_key=api_key.token)

    current_datetime = datetime.now().strftime("%d.%m.%Y-%H:%M")
    system_settings = db.query(AiSettings).filter(
        AiSettings.platform == platform,
        AiSettings.role == "system"
    ).all()

    if not system_settings:
        raise HTTPException(status_code=404, detail="System settings not found")

    system_messages = [{"role": "system", "content": setting.content} for setting in system_settings]

    system_messages.append({"role": "system", "content": f"ID клиента: {chat_id}, ID платформы: cJNYRB-WnGnvD-kACBMsQ, сегодня: {current_datetime}"})
    previous_messages = db.query(Messages).filter(Messages.chat_id == chat_id).all()
    message_history = system_messages + [
        {
            "role": "user" if message.side == "in" else "assistant",
            "content": message.text
        }
        for message in previous_messages
    ]


    # Генерируем ответ AI с возможностью вызова функций
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_history,

    )

    response_message = response.choices[0].message


    # Если функции не вызываются, возвращаем ответ AI
    generated_response = response_message.content

    # Сохраняем ответ AI в базе данных
    new_message = Messages(
        chat_id=chat_id,
        text=generated_response,
        side='out',
        business=platform
    )
    db.add(new_message)
    db.commit()

    return [generated_response]
