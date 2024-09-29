# services/ai_service.py

import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from assem.db.models import AiSettings, GTPOpen
from assem.db.models import Messages
from assem.db.crud.admin import save_bagzhan
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
    system_messages.append({"role": "system", "content": f"ID клиента: {chat_id}, сегодня: {current_datetime}"})
    previous_messages = db.query(Messages).filter(Messages.chat_id == chat_id).all()
    message_history = system_messages + [
        {
            "role": "user" if message.side == "in" else "assistant",
            "content": message.text
        }
        for message in previous_messages
    ]
    functions = [
        {
            "name": "save_bagzhan",
            "description": "Записывает лида на встречу",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {"type": "string", "description": "ID чата лида"},
                    "date": {"type": "string", "description": "Дата встречи"},
                    "note": {"type": "string", "description": "Дополнительные заметки для ИИ чтобы вспомнить и рассказать боссу"}
                },
                "required": ["chat_id", "date"]
            }
        }
        # Добавьте другие функции по необходимости
    ]

    # Генерируем ответ AI с возможностью вызова функций
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_history,
        functions=functions,
        function_call="auto",
    )

    response_message = response.choices[0].message

    # Проверяем, есть ли запрос на вызов функции
    if response_message.function_call:
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])

        if function_name == "save_bagzhan":
            # Вызываем функцию и получаем ответ
            function_response = save_bagzhan(
                chat_id=function_args.get("chat_id"),
                date=function_args.get("date"),
                note=function_args.get("note", ""),
                db=db
            )

            # Добавляем ответ функции в историю сообщений
            message_history.append({
                "role": "function",
                "name": function_name,
                "content": "Встреча успешно запланирована."
            })

            # Генерируем финальный ответ AI с учетом результата функции
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=message_history,
            )

            final_response = second_response.choices[0].message.content

            # Сохраняем ответ AI в базе данных
            new_message = Messages(
                chat_id=chat_id,
                text=final_response,
                side='out',
                business=platform
            )
            db.add(new_message)
            db.commit()

            return final_response

        else:
            # Обработка других функций
            raise HTTPException(status_code=400, detail=f"Unknown function: {function_name}")

    else:
        # Если функции не вызываются, возвращаем ответ AI
        generated_response = response_message["content"]

        # Сохраняем ответ AI в базе данных
        new_message = Messages(
            chat_id=chat_id,
            text=generated_response,
            side='out',
            business=platform
        )
        db.add(new_message)
        db.commit()

        return generated_response
