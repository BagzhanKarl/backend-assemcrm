# models/business.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from assem.db.database import Base
import datetime


class Business(Base):
    __tablename__ = "business"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(191), index=True)
    branches = Column(Integer)
    platform = Column(String(191), nullable=False)
    payment_link = Column(String(191), nullable=True)
    thanks_link = Column(String(191), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    users = relationship("User", back_populates="business")
    branch = relationship("Branch", back_populates="business")
