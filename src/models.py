import os
import sys



from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from typing import Optional
from typing import List
from sqlalchemy import create_engine
from eralchemy2 import render_er

class Base(DeclarativeBase):
    pass


association_followers = Table(
    "followers",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("follower_id", ForeignKey("users.id"), primary_key=True),
)
association_fav_posts = Table(
    "favorite_posts",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
)



class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column()
    last_name: Mapped[Optional[str]] = mapped_column() 
    user_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[int] = mapped_column()
    profile: Mapped["Profiles"] = relationship(back_populates="user")
    posts: Mapped[List["Posts"]] = relationship(secondary=association_fav_posts, back_populates="user")
    followers: Mapped[List["Users"]] = relationship(secondary=association_followers)
    comments: Mapped[List["Comments"]] = relationship(back_populates="user")

class Profiles(Base):
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[Optional[str]] = mapped_column()
    last_name: Mapped[Optional[str]] = mapped_column() 
    user_name: Mapped[str] = mapped_column()
    image_url: Mapped[Optional[str]] = mapped_column() 
    description: Mapped[str] = mapped_column
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["Users"] = relationship(back_populates="profile", single_parent=True)

    def to_dict(self):
        return {}

class Posts(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    title: Mapped[str] = mapped_column()
    text: Mapped[Optional[str]] = mapped_column()
    image_url: Mapped[Optional[str]] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(secondary=association_fav_posts, back_populates="posts")
    comments: Mapped[List["Comments"]] = relationship(back_populates="post")

class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    comment: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    
    user: Mapped["Users"] = relationship(back_populates="comments")
    post: Mapped["Posts"] = relationship(back_populates="comments")


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
