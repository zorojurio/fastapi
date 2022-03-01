from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import database, models, schemas

router = APIRouter()

get_db = database.get_db


@router.post('/user', response_model=schemas.UserOut, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = models.User(username=request.username, password=Hash.bcrypt(request.password), email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post('/users', response_model=List[schemas.UserOut], tags=["users"])
def list_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/users/{user_id}', response_model=schemas.UserOut, tags=["users"])
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
    return user
