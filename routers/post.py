from .. import models, schemas, utils
from typing import Optional, List
from fastapi import FastAPI, Response, status,HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=['Posts'])

#get posts
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

#get  posts by id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    return post

#create post
@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.CreatePost, db: Session = Depends(get_db)):
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

#update post
@router.put('/{id}',status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_post(id: int,post:schemas.UpdatePost, db: Session = Depends(get_db)):
    post_qery = db.query(models.Post).filter(models.Post.id==id)

    if not post_qery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    print(post)
    post_qery.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_qery.first()

#delete post
@router.delete('/{id}')
def delete_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    post.delete(synchronize_session=False)
    db.commit()
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
