from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

user_follow_association = Table(
    "user_follow_association",
    Base.metadata,
    Column("follower_id", ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True),
    Column("following_id", ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    username = Column(String, nullable=False, unique=True,)
    facebook_url = Column(String, nullable=True)
    twitter_url = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    youtube_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    last_actived_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text(
        'now()'), onupdate=text('now()'), nullable=False)
    
    interested_topics = relationship(
        "Topic", secondary="user_topic_association", back_populates="interested_users")
    articles = relationship("Article", back_populates="author")
    liked_articles = relationship(
        "Article",
        secondary="article_like_association",
        back_populates="liked_by"
    )
    bookmarked_articles = relationship(
        "Article",
        secondary="article_bookmark_association",
        back_populates="bookmarked_by"
    )
    following = relationship(
        "User",
        secondary=user_follow_association,
        primaryjoin=id == user_follow_association.c.follower_id,
        secondaryjoin=id == user_follow_association.c.following_id,
        back_populates="followers"
    )
    followers = relationship(
        "User",
        secondary=user_follow_association,
        primaryjoin=id == user_follow_association.c.following_id,
        secondaryjoin=id == user_follow_association.c.follower_id,
        back_populates="following"
    )
    sent_messages = relationship(
        "Message", foreign_keys='Message.sender_id', back_populates="sender")
    received_messages = relationship(
        "Message", foreign_keys='Message.receiver_id', back_populates="receiver")
    notifications = relationship("Notification",   foreign_keys="[Notification.user_id]", back_populates="user")
    triggered_notifications = relationship(
        "Notification", foreign_keys='Notification.triggered_by_id', back_populates="triggered_by")
    is_active = Column(Boolean, default=True, nullable=False)



class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text(
        'now()'), onupdate=text('now()'), nullable=False)
    
    articles = relationship(
        "Article", secondary="article_topic_association", back_populates="topic")
    interested_users = relationship(
        "User", secondary="user_topic_association", back_populates="interested_topics")



class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    cover_image = Column(String, nullable=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    topic_id = Column(Integer, ForeignKey(
        'topics.id', ondelete='SET NULL'), nullable=True)
    views_count = Column(Integer, default=0, nullable=False)
    reading_time = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text(
        'now()'), onupdate=text('now()'), nullable=False)

    topic = relationship(
        "Topic", secondary="article_topic_association", back_populates="articles")
    author = relationship("User", back_populates="articles")

    liked_by = relationship(
        "User",
        secondary="article_like_association",
        back_populates="liked_articles"
    )
    bookmarked_by = relationship(
        "User",
        secondary="article_bookmark_association",
        back_populates="bookmarked_articles"
    )
    comments = relationship(
        "Comment", back_populates="article", cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey(
        "articles.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey(
        "comments.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text(
        "now()"), onupdate=text("now()"), nullable=False)

    user = relationship("User")
    article = relationship("Article", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=True)  # Optional caption
    is_read = Column(Boolean, default=False)
    read_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), onupdate=text("now()"))

    sender = relationship("User", foreign_keys=[
                          sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[
                            receiver_id], back_populates="received_messages")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # "like", "follow", "comment"
    user_id = Column(Integer, ForeignKey("users.id"),
                     nullable=False)  # who receives it
    triggered_by_id = Column(Integer, ForeignKey(
        "users.id"), nullable=False)  # who triggered it
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("now()"), onupdate=text("now()"))
    is_read = Column(Boolean, default=False)

    
    user = relationship("User", foreign_keys=[user_id], back_populates="notifications")
    triggered_by = relationship("User", foreign_keys=[triggered_by_id], back_populates="triggered_notifications")


user_topic_association = Table(
    "user_topic_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", Integer, ForeignKey(
        "topics.id", ondelete="CASCADE"), primary_key=True),

)


article_topic_association = Table(
    "article_topic_association",
    Base.metadata,
    Column("article_id", Integer, ForeignKey(
        "articles.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", Integer, ForeignKey(
        "topics.id", ondelete="CASCADE"), primary_key=True)
)

article_like_association = Table(
    "article_like_association",
    Base.metadata,
    Column("user_id", ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True),
    Column("article_id", ForeignKey("articles.id",
           ondelete="CASCADE"), primary_key=True),
)

article_bookmark_association = Table(
    "article_bookmark_association",
    Base.metadata,
    Column("user_id", ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True),
    Column("article_id", ForeignKey("articles.id",
           ondelete="CASCADE"), primary_key=True),
)
