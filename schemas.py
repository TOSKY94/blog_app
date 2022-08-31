from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title :str
    content : str
    published : bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class Post(PostBase):
    id :int
    create_date: datetime

    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    create_date: datetime
    class Config:
        orm_mode = True

class token(BaseModel):
    access_token:str
    token_type:str

class tokenData(BaseModel):
    id: Optional[str] = None
