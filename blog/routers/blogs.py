from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from .. import database, schemas
from .. import outh2
from ..repository import blogs

router = APIRouter(
    prefix="/blog",
    tags=['blogs'],
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blogs.create(db, request)


@router.get('/', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(outh2.get_current_user)):
    return blogs.get_all(db=db)


@router.get('/{blog_id}', status_code=200, response_model=schemas.ShowBlog)
def blog_detail(blog_id: int, db: Session = Depends(get_db)):
    return blogs.show(blog_id, db)


@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id, db: Session = Depends(get_db)):
    return blogs.destroy(blog_id, db)


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    return blogs.update(blog_id, db, request)
