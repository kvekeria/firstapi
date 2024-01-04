from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from . import schemas
from datetime import datetime, timedelta
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

key = settings.secret_key
algo = settings.algorithm
time = settings.access_token_expire_minutes

def create_token(data: dict):
    to_encode = data.copy()
    expiretime = datetime.utcnow() + timedelta(minutes=time)
    to_encode.update({"exp": expiretime})
    return jwt.encode(to_encode, key, algo)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, key, algo)
        id = payload.get('id')
        data = schemas.TokenData(id=id)
        return data
    except JWTError:
        raise credentials_exception