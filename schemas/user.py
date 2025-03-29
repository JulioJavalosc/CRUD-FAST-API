from pydantic import BaseModel
from typing import Optional, List


class UserCreate(BaseModel):
    name: str
    email: str
    password:str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserValidate(BaseModel):
    name: str
    password: str
    email:str
    class Config:
        from_attributes = True