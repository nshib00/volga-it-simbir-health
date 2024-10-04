from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from timetable.app.database import Base


class Timetable(Base):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True)
    hospitalId = Column(Integer, nullable=False)
    doctorId = Column(Integer)
    from_ = Column(DateTime)
    to = Column(DateTime)
    room = Column(String, nullable=False)


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    timetable_id = Column(Integer, ForeignKey('timetables.id'))
    from_ = Column(DateTime)
    to = Column(DateTime)