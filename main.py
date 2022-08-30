from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2

app = FastAPI()
posts = [{"id":1, "title":"title of post 1", "content":"content of post 1"},
 {"id":2, "title":"title of post 2", "content":"content of post 2"}]

class post(BaseModel):
    title: str
    content: str
    published:bool = True


#get posts
@app.get('/posts')
def get_posts():
    return {"message":"sucess", "data":posts}

#get  posts by id
@app.get('/posts/{id}')
def get_posts():
    return {"message":"sucess", "data":posts}

#create post
@app.post('/posts/create')
def get_posts():
    return {"message":"sucess", "data":posts}

#update post
@app.put('/posts/{id}')
def get_posts():
    return {"message":"sucess", "data":posts}

#delete post
@app.delete('/posts/{id}')
def get_posts():
    return {"message":"sucess", "data":posts}