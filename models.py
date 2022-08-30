from email import contentmanager
from email.policy import default
from tokenize import String
from turtle import title
from xmlrpc.client import Boolean
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
