from fastapi import FastAPI

from . import models
from .database import engine
from .routers import blogs, users, auth

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
    {
        "name": "authentication",
        "description": "Manage Authentication. JWT Tokens are handled here.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(auth.router)
