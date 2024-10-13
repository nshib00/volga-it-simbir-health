from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import column_property

from account.app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(20), nullable=False)
    lastName = Column(String(50), nullable=False)
    username = Column(String(30), nullable=False)
    hashed_password = Column(String, nullable=False)
    roles = Column(JSON, default=['User'])

    fullName = column_property(firstName + ' ' + lastName)



