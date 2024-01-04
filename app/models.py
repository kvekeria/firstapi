from .database import Base
from sqlalchemy import TIMESTAMP, Integer, String, Boolean, ForeignKey, Column, text
from sqlalchemy.orm import relationship
from pydantic import EmailStr
from datetime import datetime

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    
    user = relationship('User')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = 'votes'
    
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
