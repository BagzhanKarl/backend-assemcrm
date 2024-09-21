# models/user.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from assem.db.database import Base

import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(11), unique=True, index=True)
    first_name = Column(String(191), nullable=True)
    last_name = Column(String(191), nullable=True)
    role_id = Column(Integer, ForeignKey('system_role.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    business_id = Column(Integer, ForeignKey('business.id'), nullable=True)
    hashed_password = Column(String(191), nullable=True)

    business = relationship("Business", back_populates="users")
    role = relationship("Role", back_populates="users")
