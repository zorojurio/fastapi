from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import database, models, schemas

router = APIRouter(
    prefix="/blog",
    tags=['blogs'],
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    print(new_blog)
    return new_blog


@router.get('/', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/{blog_id}', status_code=200, response_model=schemas.ShowBlog)
def blog_detail(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the {blog_id} is not available"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} is not found")
    return blog


@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {blog_id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {blog_id} not found")
    blog.update(request.dict())
    db.commit()
    return blog.first()
