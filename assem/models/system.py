# models/system.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from assem.db.database import Base

class Role(Base):
    __tablename__ = "system_role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(191), index=True)

    users = relationship("User", back_populates="role")

class Category(Base):
    __tablename__ = 'system_category'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(191), nullable=False)

    system_type = relationship("Type", back_populates="category")

class Type(Base):
    __tablename__ = 'system_type'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(191), nullable=False)
    category_id = Column(Integer, ForeignKey('system_category.id'), nullable=True)

    category = relationship("Category", back_populates="system_type")
