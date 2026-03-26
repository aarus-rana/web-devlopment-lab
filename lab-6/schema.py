from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TodoCreate(BaseModel):
    text: str
    completed: bool = False

class TodoUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    text: str
    completed: bool
    user_id: int
