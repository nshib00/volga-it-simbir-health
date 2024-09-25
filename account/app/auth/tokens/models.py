from sqlalchemy import Column, ForeignKey, Integer, String

from account.app.database import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    value = Column(String, nullable=False)