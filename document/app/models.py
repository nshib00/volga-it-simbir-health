from sqlalchemy import Column, DateTime, Integer, String
from document.app.database import Base



class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    pacientId = Column(Integer, nullable=False)
    hospitalId = Column(Integer, nullable=False)
    doctorId = Column(Integer, nullable=False)
    room = Column(String, nullable=False)
    data = Column(String)

    