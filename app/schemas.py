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
    profile_image: Optional[str] = None
    class Config:
        from_attributes = True
class AuthUserOut(UserBase):
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

class SingleTopic(BaseModel):
    topic: str

class TopicOut(TopicBase):
    id: int
    created_at: datetime
    interested_users: list[UserOut] = []
    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    user: UserOut
    parent_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ArticleBase(BaseModel):
    title: str
    content: str
    cover_image: Optional[str] = None
    reading_time: Optional[int] = None
    is_published: bool = False

class ArticleCreate(ArticleBase):
    topics: list[str] = []

class ArticleOut(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    comments: list[CommentOut] = []
    views_count: int = 0
    likes_count: int = 0
    bookmark_count: int = 0
    author: UserOut
    bookmarked_by: list[UserOut] = []
    liked_by: list[UserOut] = []
    topic: list[TopicOut] = []
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class UserDashboard(BaseModel):
    id: int
    email: EmailStr
    username: str
    topics: list[TopicOut] = []
    articles: list[ArticleOut] = []
    articles_count: int = Field(0, ge=0)
    followers_count: int = Field(0, ge=0)
    following_count: int = Field(0, ge=0)
    followers: list[UserOut] = []
    following: list[UserOut] = []
    twitter_url: Optional[str] = None
    instagram_url: Optional[str] = None
    website_url: Optional[str] = None
    youtube_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageOut(MessageBase):
    id: int
    created_at: datetime
    sender_id: int
    receiver_id: int
    class Config:
        from_attributes = True


