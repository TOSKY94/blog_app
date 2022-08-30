from http.client import HTTPException
from random import randrange
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()
posts = [{"id":1, "title":"title of post 1", "content":"content of post 1"},
 {"id":2, "title":"title of post 2", "content":"content of post 2"}]

class post(BaseModel):
    id:int = None
    title: str
    content: str = None


@app.get('/posts')
def get_posts():
    return {"message":"sucess", "data":posts}

@app.get('/post/{id}')
def get_posts(id: int, response: Response):
    for post in posts:
        if (post['id']==int(id)):
            return {"message":"sucess", "data":post}
    response.status_code=status.HTTP_400_BAD_REQUEST
    return {"message":"No data found", "data":[]}   
    
@app.delete('/post/delete/{id}')
def delete_post(id: int, response:Response):
    if id==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    for idx, post in enumerate(posts):
        if (post['id']==int(id)):
            posts.pop(idx)
            return {"message":"sucess"}
    response.status_code=status.HTTP_400_BAD_REQUEST
    return {"message":"No data found", "data":[]}    

@app.post('/post')
def create_post(payload: post):
    post_dict = payload.dict()
    post_dict['id'] = randrange(1,99999)
    posts.append(post_dict)
    return {"message":"sucess", "data":post_dict}
