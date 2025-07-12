from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AuthUserOut(UserBase):
    id: int
    created_at: datetime
    access_token: Optional[str] = None
    token_type: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    email: str

class TopicBase(BaseModel):
    title: str

class TopicCreate(TopicBase):
    pass

class TopicOut(TopicBase):
    id: int
    created_at: datetime
    interested_users: list[UserOut] = []

    class Config:
        from_attributes = True

class ArticleBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    author_id: int

class ArticleCreate(ArticleBase):
    topics: list[TopicCreate] = []

class ArticleOut(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True


class UserDashboard(BaseModel):
    user: UserOut
    topics: list[TopicOut] = []
    articles: list[ArticleOut] = []
    feeds: list[ArticleOut] = []
    articles_count: int = Field(0, ge=0)

    class Config:
        from_attributes = True
