from .. import models, schemas, utils
from typing import Optional, List
from fastapi import FastAPI, Response, status,HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter()

#create user
@router.post('/users/create', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.User, db: Session = Depends(get_db)):
    #hash password
    user.password = utils.hash_password(user.password)
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#get  user by id
@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_post(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    return user