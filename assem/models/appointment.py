from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from assem.db.database import Base

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True)
    master_id = Column(Integer, ForeignKey("masters.id"))
    branch_id = Column(Integer, ForeignKey("branches.id"))
    business_id = Column(Integer, ForeignKey("businesses.id"))
    duration = Column(Integer)
    start_time = Column(String)
    end_time = Column(String)
    timezone = Column(String)
    is_canceled = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)

    master = relationship("Master")
    branch = relationship("Branch")
    business = relationship("Business")
