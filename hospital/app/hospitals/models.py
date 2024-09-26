from sqlalchemy import JSON, Column, Integer, String

from hospital.app.database import Base


class Hospital(Base):
    __tablename__ = 'hospitals'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    contactPhone = Column(String(20), nullable=False)
    rooms = Column(JSON, default=[])