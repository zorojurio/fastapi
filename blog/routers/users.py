from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import database, models, schemas
from ..hashing import Hash
from ..repository import users
router = APIRouter(
    prefix="/user",
    tags=["users"]
)

get_db = database.get_db


@router.post('/', response_model=schemas.UserOut)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return users.create(db, request)


@router.get('/', response_model=List[schemas.UserOut])
def list_user(db: Session = Depends(get_db)):
    return users.get_all(db)


@router.get('/{user_id}', response_model=schemas.UserOut)
def user_detail(user_id: int, db: Session = Depends(get_db)):
    return users.show(user_id, db)
