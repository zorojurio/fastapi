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


class UserOut(BaseModel):
    username: str
    email: str
    blogs: List[Blog]

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: UserOut

    class Config:
        orm_mode = True
