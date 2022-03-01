from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, SessionLocal
from .hashing import Hash

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blogs', status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    print(new_blog)
    return new_blog


@app.get('/blogs', response_model=List[schemas.ShowBlog], tags=["blogs"])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blogs/{blog_id}', status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
def blog_detail(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the {blog_id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} is not found")
    return blog


@app.delete('/blogs/{blog_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {blog_id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


@app.put('/blogs/{blog_id}', status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {blog_id} not found")
    blog.update(request.dict())
    db.commit()
    return blog.first()


@app.post('/user', response_model=schemas.UserOut, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = models.User(username=request.username, password=Hash.bcrypt(request.password), email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post('/users', response_model=List[schemas.UserOut], tags=["users"])
def list_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/users/{user_id}', response_model=schemas.UserOut, tags=["users"])
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
    return user


