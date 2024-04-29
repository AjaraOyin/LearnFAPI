from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)


@router.get("/", response_model=List[schemas.ResPost])
def getpost(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.ResPost)
def createpost(newpost : schemas.createPost, db: Session = Depends(get_db)):
    posts = models.Post(**newpost.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts


@router.get("/{id}", response_model=schemas.ResPost)
def get_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f'post with {id} was not found')
        
    return posts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    
    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} does not exist")
    posts.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_post(id: int, Post: schemas.createPost, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id)

    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with the id {id} does not exist")
    posts.update(Post.dict(), synchronize_session=False)
    db.commit()
    return posts.first()