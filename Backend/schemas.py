from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import TaskStatus
# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
# Subject schemas
class SubjectBase(BaseModel):
    name: str
    color_hex: Optional[str] = "#CCCCCC"
class SubjectCreate(SubjectBase):
    pass
class SubjectUpdate(SubjectBase):
    pass
class SubjectResponse(SubjectBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_minutes: Optional[int] = 60
    subject_id: Optional[int] = None
class TaskCreate(TaskBase):
    pass
class TaskUpdate(TaskBase):
    status: Optional[TaskStatus] = None
    title: Optional[str] = None
    description: Optional[str] = None
    estimated_minutes: Optional[int] = None
    subject_id: Optional[int] = None
class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    user_id: int
    is_ai_suggested: bool
    
    class Config:
        from_attributes = True
# Auth token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    email: Optional[str] = None
