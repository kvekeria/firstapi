from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from .. import schemas
from typing import List
from ..utils import hash

router = APIRouter(
    prefix = '/users',
    tags = ['Users']
)

@router.get('/', response_model=List[schemas.ReturnUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'No users exist!')
    return users

@router.get('/{id}', response_model=schemas.ReturnUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found!')
    return user

@router.post('/', response_model=schemas.ReturnUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Email already used on another account!')
    password = hash(user.password)
    print(password)
    user = User(email=user.email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'cannot perform requested action!')
    return user

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found!")
    user.delete(synchronize_session=False)
    db.commit()