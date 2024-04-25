from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas, util
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()




# @app.get("/sql")
# def test_post(db: Session = Depends(get_db)):

#     posts = db.query(models.Post).all()
#     return{"data": posts} 


@app.get("/posts", response_model=List[schemas.ResPost])
def getpost(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.ResPost)
def createpost(newpost : schemas.createPost, db: Session = Depends(get_db)):
    posts = models.Post(**newpost.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts


@app.get("/posts/{id}", response_model=schemas.ResPost)
def get_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f'post with {id} was not found')
        
    return posts

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    
    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} does not exist")
    posts.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, Post: schemas.createPost, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id)

    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} does not exist")
    posts.update(Post.dict(), synchronize_session=False)
    db.commit()
    return posts.first()


@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.Userout)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):

    hashedpassword=util.hash(user.password)
    user.password=hashedpassword

    users = models.User(**user.dict())
    db.add(users)
    db.commit()
    db.refresh(users)
    return users
