#from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


#class Role(str, Enum):
    # ADMIN = "admin"
    # USER = "user"

##userlogin
class UserLogin(BaseModel):
    email: EmailStr
    password: str
   


# User Schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    role: str
    created_by: int
    #role: Role

# Task Schema
class TaskCreate(BaseModel):
    activity: str
    Status: str
    user_id: int
    isExisted: Optional[bool] = True

class TaskResponse(BaseModel):
    id: int
    activity: str
    Status: str
    user_id: int
    isExisted: bool
    Time_Created: datetime

    class config:
        orm_mode = True

#USER-TASK

class UserTaskResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    tasks: List[TaskResponse]