import time
from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class post(BaseModel):
    title: str
    content: str
    published:bool = True

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapiDB', user='postgres', password='1234',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successful...')
        break
    except Exception as err:
        print(f'database connection failed: {err}')
        time.sleep(3)


#get posts
@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"message":"sucess", "data":posts}

#get  posts by id
@app.get('/posts/{id}')
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts where id=%s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    return {"message":"sucess", "data":post}

#create post
@app.post('/posts/create')
def create_post(post:post):
    cursor.execute("""INSERT INTO posts("title", "content",published) 
                        VALUES(%s,%s,%s)""",(post.title, post.content, post.published))
    conn.commit()
    post = cursor.fetchone
    return {"message":"sucess", "data":post}

#update post
@app.put('/posts/{id}')
def update_post(id: int,post: post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",
                    (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    conn.commit()
    return {"message":"record updated", "data":post}

#delete post
@app.delete('/posts/{id}')
def delete_post(id):
    cursor.execute("""DELETE FROM posts where id=%s RETURNING *""",(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='record not found')
    conn.commit()
    return {"message":"record deleted", "data":post}