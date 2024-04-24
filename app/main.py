from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class post(BaseModel):
   title: str
   content: str
   published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', 
                                password='password', cursor_factory= RealDictCursor )
        cursor = conn.cursor()
        print("Database connection was successful")
        break

    except Exception as error:
        print("Database connection failed")
        print('the error was:', error)
        time.sleep(2)



mypost = [{"titl": "1st Post", "content": "Contents of the 1st post", "id":1}, 
          {"titl": "2nd Post", "content": "Contents of the 2nd post", "id":2}]

def find_post(id):
    for p in mypost:
        if p['id'] == id:
            return p
        
def find_indexpost(id):
    for i,p in enumerate(mypost):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def getpost():
    cursor.execute("""SELECT * FROM post""")
    post= cursor.fetchall()

    return {"message": post}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def createpost(newpost : post):
    cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (newpost.title, newpost.content, newpost.published))
    new_post = cursor.fetchone()
    conn.commit()
    # print(newpost)
    # print(newpost.dict())
    # post_dict = newpost.dict()
    # post_dict['id'] = randrange(0, 10000)
    # mypost.append(post_dict)
    return {"newPost": new_post}

# @app.get("/posts/latest")
# def latest_post():
#     post = mypost[len(mypost)-1]
#     return {'latest_post': post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f'post with {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with {id} was not found'}
    return {"post_datail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, Post: post):
    cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s Returning *""", 
                   (Post.title, Post.content, Post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} does not exist")
    return {'data': updated_post}


   