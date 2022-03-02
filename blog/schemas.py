from typing import List

from pydantic import BaseModel


class BaseBlog(BaseModel):
    title: str
    body: str


class Blog(BaseBlog):
    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    password: str
    email: str


class UserOutBase(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserOut(UserOutBase):
    blogs: List[Blog]


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: UserOutBase

    class Config:
        orm_mode = True
