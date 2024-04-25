from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app  = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None


my_posts = [{"title":"title of post 1", "content":"content of post 1","id":1}, {"title":"favorite foods","content":"I like pizza","id":2}]

def find_post(id):
  for p in my_posts:
    if p["id"]==id:
      return p

def find_index_post(id):
  for idx, p in enumerate(my_posts):
    if p['id']==id:
      return idx
    
@app.get("/")
def root():
  return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
  return {"data":my_posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
  post_dict = post.model_dump()
  post_dict['id'] = randrange(0,1000000)
  my_posts.append(post_dict)
  return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
  post = find_post(id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found!")
  return {"post_detail":post}


@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  #deleting a post with id 1
  #find the index of the array with has required ID
  index = find_index_post(id)
  #raise exeception if you can't find the post
  if index==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
  my_posts.pop(index)
  #when you delete something you don't want to return any data, just return the 204 status code
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  print(post)
  index = find_index_post(id)
  #raise exeception if you can't find the post
  if index==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
  post_dict = post.model_dump()
  post_dict["id"] = id
  my_posts[index] = post_dict
  return {"data": post_dict}
