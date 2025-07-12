from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
class UserCreate(UserBase):
    password: str
class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    facebook_url: Optional[str] = None
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    website_url: Optional[str] = None
    youtube_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    profile_image: Optional[str] = None
    last_actived_at: Optional[datetime] = None
    interested_topics: Optional[list[int]] = Field(default_factory=list)
    class Config:
        from_attributes = True

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

class TopicBase(BaseModel):
    title: str

class TopicCreate(BaseModel):
    topics: list[str] = []
    
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
