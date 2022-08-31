from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import models, schemas, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

#authenticate user
@router.post('/login', status_code=status.HTTP_201_CREATED)
def login(user_cred:schemas.User, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email==user_cred.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    if not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    #create token
    #return token
    return {"token":"xyz"}
