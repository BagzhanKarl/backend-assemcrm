from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from assem.db.database import Base

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("business.id"))
    city = Column(String(191))
    address = Column(String(191))
    admin_id = Column(Integer, ForeignKey("users.id"))

    business = relationship("Business", back_populates="branches")
    admin = relationship("User", back_populates="branches")
