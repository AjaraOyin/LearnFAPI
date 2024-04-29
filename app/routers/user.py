from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db

from .. import models, schemas, util

router = APIRouter(
    prefix= "/users",
    tags= ['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Userout)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):

    hashedpassword=util.hash(user.password)
    user.password=hashedpassword

    users = models.User(**user.dict())
    db.add(users)
    db.commit()
    db.refresh(users)
    return users


@router.get("/{id}", response_model=schemas.Userout)
def get_user(id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()
    
    if not users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f'post with {id} was not found')
        
    return users