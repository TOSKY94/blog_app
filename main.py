import time
from fastapi import FastAPI, Response, status,HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#get posts
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"message":"sucess", "data":posts}

#get  posts by id
@app.get('/posts/{id}')
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    return {"message":"sucess", "data":post}

#create post
@app.post('/posts/create')
def create_post(post:schema.CreatePost, db: Session = Depends(get_db)):
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message":"sucess", "data":post}

#update post
@app.put('/posts/{id}')
def update_post(id: int,post:schema.UpdatePost, db: Session = Depends(get_db)):
    post_qery = db.query(models.Post).filter(models.Post.id==id)

    if not post_qery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    print(post)
    post_qery.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"message":"record updated", "data": post_qery.first()}

#delete post
@app.delete('/posts/{id}')
def delete_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    post.delete(synchronize_session=False)
    db.commit()
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
