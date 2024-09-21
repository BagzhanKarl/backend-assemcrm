from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from assem.db.database import Base


class Master(Base):
    __tablename__ = "masters"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    branch_id = Column(Integer, ForeignKey("branches.id"))

    business = relationship("Business", back_populates="masters")
    user = relationship("User", back_populates="masters")
    branch = relationship("Branch", back_populates="masters")
    schedules = relationship("Schedule", back_populates="master")
