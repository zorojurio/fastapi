from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..hashing import Hash


def create(db: Session, request: schemas.User):
    user = models.User(username=request.username, password=Hash.bcrypt(request.password), email=request.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def show(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
    return user
