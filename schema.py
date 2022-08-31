from datetime import datetime
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
    class Config:
        orm_mode = True