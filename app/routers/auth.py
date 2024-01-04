from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from .. import schemas
from typing import List
from ..utils import hash, verify
from ..oauth2 import create_token

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login_user(login: schemas.LoginUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login.email).first()
    if not user or not verify(login.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials!')
    access_token = create_token({"id": user.id})
    return {"access_token": access_token}