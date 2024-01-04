from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = True

class CreatePost(Post):
    pass

class ReturnUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode: True

class ReturnPost(Post):
    user_id: int
    user: ReturnUser
    id: int
    created_at: datetime

    class Config:
        orm_mode: True

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = 'bearer'

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    vote_dir: bool

class PostOut(Post):
    Post: ReturnPost
    votes: int

    class Config:
        orm_mode: True