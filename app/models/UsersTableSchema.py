from db.base import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, func

class UsersTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=64), nullable=False, unique=True)
    password = Column(Text, unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
