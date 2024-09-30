# services/ai_service.py

import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from assem.db.models import AiSettings, GTPOpen
from assem.db.models import Messages
from assem.db.crud.admin import save_bagzhan, find_meetings_by_date, cancel_meeting, check_user_has_meeting, \
    check_meeting_on_date
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

    if chat_id == '77761174378@s.whatsapp.net':
        system_messages.append({"role": "system", "content": f"ID пользователя: {chat_id}, сегодня: {current_datetime}. Это твой босс. Его имя Багжан. Кроме него у тебя нету босса в этой компаний!"})
    else:
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
                    "note": {"type": "string",
                             "description": "Дополнительные заметки для ИИ чтобы вспомнить и рассказать боссу, например, Имя клиента и так далее"}
                },
                "required": ["chat_id", "date"]
            }
        },
        {
            "name": "check_meeting_on_date",
            "description": "Проверяет, есть ли встреча на указанную дату для лида",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {"type": "string", "description": "ID чата лида"},
                    "date": {"type": "string", "description": "Дата встречи"}
                },
                "required": ["chat_id", "date"]
            }
        },
        {
            "name": "check_user_has_meeting",
            "description": "Проверяет, есть ли у пользователя запланированная встреча",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {"type": "string", "description": "ID чата лида"}
                },
                "required": ["chat_id"]
            }
        },
        {
            "name": "cancel_meeting",
            "description": "Отменяет (удаляет) встречу на указанную дату",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {"type": "string", "description": "ID чата лида"},
                    "date": {"type": "string", "description": "Дата встречи"}
                },
                "required": ["chat_id", "date"]
            }
        },
        {
            "name": "find_meetings_by_date",
            "description": "Ищет все встречи на определенную дату",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Дата для поиска встреч"}
                },
                "required": ["date"]
            }
        }
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
        function_name = response_message.function_call.name
        function_args = json.loads(response_message.function_call.arguments)

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

        elif function_name == "check_meeting_on_date":
            # Проверяем наличие встречи на указанную дату
            meeting_exists = check_meeting_on_date(
                chat_id=function_args.get("chat_id"),
                date=function_args.get("date"),
                db=db
            )

            if meeting_exists:
                function_response = "Встреча уже запланирована на эту дату."
            else:
                function_response = "Встреча на эту дату не найдена."

            message_history.append({
                "role": "function",
                "name": function_name,
                "content": function_response
            })

        elif function_name == "check_user_has_meeting":
            # Проверяем наличие у пользователя запланированных встреч
            user_has_meeting = check_user_has_meeting(
                chat_id=function_args.get("chat_id"),
                db=db
            )

            if user_has_meeting:
                function_response = "У пользователя есть запланированные встречи."
            else:
                function_response = "У пользователя нет запланированных встреч."

            message_history.append({
                "role": "function",
                "name": function_name,
                "content": function_response
            })

        elif function_name == "cancel_meeting":
            # Отменяем встречу
            function_response = cancel_meeting(
                chat_id=function_args.get("chat_id"),
                date=function_args.get("date"),
                db=db
            )

            message_history.append({
                "role": "function",
                "name": function_name,
                "content": function_response
            })

        elif function_name == "find_meetings_by_date":
            # Ищем встречи по дате
            meetings = find_meetings_by_date(
                date=function_args.get("date"),
                db=db
            )

            if meetings:
                function_response = f"Найдено {len(meetings)} встреч на эту дату."
            else:
                function_response = "Встреч на эту дату не найдено."

            message_history.append({
                "role": "function",
                "name": function_name,
                "content": function_response
            })

        else:
            # Обработка неизвестной функции
            raise HTTPException(status_code=400, detail=f"Unknown function: {function_name}")

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

        return generated_response
