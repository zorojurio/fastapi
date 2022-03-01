from fastapi import FastAPI

from . import models
from .database import engine
from .routers import blogs, users

models.Base.metadata.create_all(bind=engine)
print("creating")
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "blogs",
        "description": "Manage blogs. So _fancy_ they have their own docs.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(blogs.router)
app.include_router(users.router)
