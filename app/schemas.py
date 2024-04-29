from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
   title: str
   content: str
   published: bool = True

class createPost(PostBase):
    pass


class ResPost(PostBase):
    # id: int
    # created_at: datetime
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class Userout(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None