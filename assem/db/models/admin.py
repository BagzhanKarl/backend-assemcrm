# models/branch.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from assem.db.database import Base
import datetime

class Bagzhan(Base):
    __tablename__ = 'bagzhan'

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(255))
    date = Column(String(255))
    note = Column(String(255))
    is_completed = Column(Boolean)