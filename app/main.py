from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app  = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True

while True:
  #while loop so that we don't move forward unless the database connection is successful
  try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Deeper31145@',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful!")
    break
  except Exception as error:
    print("Database connection failed")
    print("Error was: ",error)
    time.sleep(2)


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
  cursor.execute("""SELECT * FROM POSTS """)
  posts = cursor.fetchall()
  return {"data":posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
  cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
  new_post = cursor.fetchone()
  conn.commit()
  return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
  cursor.execute("""Select * from posts where id=%s""",str(id))
  post = cursor.fetchone()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found!")
  return {"post_detail":post}


@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  cursor.execute("""DELETE FROM posts where id=%s returning * """,str(id))
  deleted_post = cursor.fetchone()
  if deleted_post==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
  conn.commit()
  #when you delete something you don't want to return any data, just return the 204 status code
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  cursor.execute("""UPDATE posts SET title=%s,content=%s where id=%s returning *""",(post.title,post.content,str(id)))
  updated_post = cursor.fetchone()
  #raise exeception if you can't find the post
  if updated_post==None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
  conn.commit()
  return {"data": updated_post}
