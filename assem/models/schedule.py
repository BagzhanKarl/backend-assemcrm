from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from assem.db.database import Base


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    master_id = Column(Integer, ForeignKey("masters.id"))
    date = Column(String(191))
    work_time_at = Column(String(191))
    work_time_on = Column(String(191))
    break_time_at = Column(String(191))
    break_time_on = Column(String(191))

    master = relationship("Master", back_populates="schedules")
