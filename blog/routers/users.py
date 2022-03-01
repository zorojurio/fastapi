from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import database, models, schemas
from ..hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

get_db = database.get_db


@router.post('/', response_model=schemas.UserOut)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = models.User(username=request.username, password=Hash.bcrypt(request.password), email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/', response_model=List[schemas.UserOut])
def list_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{user_id}', response_model=schemas.UserOut)
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
    return user
