# models/user.py
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from assem.db.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    phone = Column(String(11), nullable=False)
    role_id = Column(Integer, ForeignKey('system_role.id'), nullable=False)
    business_id = Column(Integer, ForeignKey('business.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    role = relationship('Role', back_populates='user')
    business = relationship('Business', back_populates='user')