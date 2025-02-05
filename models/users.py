from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

# class Role(str, Enum):  # Define Role enum (same as in schemas)
#     ADMIN = "admin"
#     USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    created_by = Column(Integer, nullable=False)


    tasks = relationship("Tasks", back_populates="user")

class Tasks(Base):
    __tablename__ =  "TODO"
    id = Column(Integer, primary_key = True, autoincrement=True)
    activity = Column(String(255), nullable=False)
    Status = Column(String(255), nullable=False)
    isExisted = Column(Boolean, nullable = False, default = True)
    Time_Created =Column(DateTime, default = func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="tasks")