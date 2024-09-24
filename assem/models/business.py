# models/user.py
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from assem.db.database import Base

class Business(Base):
    __tablename__ = 'business'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), nullable=False)
    branch = Column(Integer, nullable=False, default=1)
    type_id = Column(Integer, ForeignKey('system_type.id'), nullable=False)


    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    user = relationship('User', back_populates='business')
    type = relationship('Type', 'business')


