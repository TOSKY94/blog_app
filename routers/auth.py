from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, utils,oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

#authenticate user
@router.post('/login', status_code=status.HTTP_201_CREATED)
def login(user_cred:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email==user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"token":access_token, "token_type":"bearer"}
