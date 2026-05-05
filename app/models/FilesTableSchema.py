from db.base import Base
from sqlalchemy import Column, Index, Integer, DateTime, func, String, ForeignKey
from sqlalchemy.orm import relationship

class FilesTable(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(length=64), unique=False, nullable=False)
    section = Column(String(length=32), nullable=False)
 
    user = relationship("Users", back_populates="files")
    __table_args__ = (Index("ix_file_id", id),)