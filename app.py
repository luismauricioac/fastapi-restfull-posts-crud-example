# FastApi Crud Example
# Following the youtube video on https://www.youtube.com/watch?v=_eWEmRWhk9A&ab_channel=FaztCode by FaztCode

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Text
from typing import Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

posts = []

# Post Model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

@app.get('/')
def read_root():
    return {"welcome": "Welcome to my REST API"}

@app.get('/posts')
def get_posts():
    return posts


@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1] # return the last element

@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="post not found")

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted successfully"}
    raise HTTPException(status_code=404, detail="post not found")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updated_post_aux: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updated_post_aux.title
            posts[index]["content"] = updated_post_aux.content
            posts[index]["author"] = updated_post_aux.author
            return {"message": "Post has been updated successfully"}
    raise HTTPException(status_code=404, detail="post not found")