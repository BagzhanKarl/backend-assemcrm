from sqlalchemy import Integer, String, Boolean, ForeignKey, Column
from sqlalchemy.orm import relationship
from assem.db.database import Base

class Branch(Base):
    __tablename__ = 'branch'

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(60), nullable=False)
    city = Column(String(60), nullable=False)
    street = Column(String(60), nullable=False)
    home = Column(String(60), nullable=False)

    business_id = Column(Integer, ForeignKey('business.id'), nullable=False)

    business = relationship('Business', back_populates='branch')
