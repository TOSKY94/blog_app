import time
from typing import Optional, List
from fastapi import FastAPI, Response, status,HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schema, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#get posts
@app.get('/posts', status_code=status.HTTP_200_OK, response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

#get  posts by id
@app.get('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schema.Post)
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    return post

#create post
@app.post('/posts/create', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post:schema.CreatePost, db: Session = Depends(get_db)):
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

#update post
@app.put('/posts/{id}',status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def update_post(id: int,post:schema.UpdatePost, db: Session = Depends(get_db)):
    post_qery = db.query(models.Post).filter(models.Post.id==id)

    if not post_qery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    print(post)
    post_qery.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_qery.first()

#delete post
@app.delete('/posts/{id}')
def delete_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    post.delete(synchronize_session=False)
    db.commit()
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#create user
@app.post('/users/create', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user:schema.User, db: Session = Depends(get_db)):
    #hash password
    user.password = utils.hash_password(user.password)
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
