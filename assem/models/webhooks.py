# models/webhooks.py
from sqlalchemy import Column, String, Integer, JSON, Boolean
from assem.db.database import Base

class Whatsapp(Base):
    __tablename__ = 'whatsapp_web'

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(255), index=True)  # ID сообщения
    chat_id = Column(String(255))                  # ID чата
    sender = Column(String(255))                   # Отправитель
    sender_name = Column(String(255))              # Имя отправителя
    message_type = Column(String(255))             # Тип сообщения (text)
    timestamp = Column(String(255))               # Временная метка
    text_body = Column(String(255))                # Текст сообщения
    channel_id = Column(String(255))               # ID канала
    status = Column(Boolean, default=False)
