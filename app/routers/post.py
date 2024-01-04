from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db), user: dict = Depends(get_current_user), limit: int = 10):
    posts = db.query(models.Post).limit(limit).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    print(results)
    if not posts:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'No Posts Available!')
    return results

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find post!')
    
@router.post('/', response_model=schemas.ReturnPost)
def create_post(post: schemas.CreatePost, db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    new_post = models.Post(user_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put('/{id}', response_model=schemas.ReturnPost)
def create_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'requested action cannot be completed!')
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find post!')
    query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def create_post(id: int, db: Session = Depends(database.get_db), user: dict = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first().user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'requested action cannot be completed!')
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find post!')
    post.delete(synchronize_session=False)
    db.commit()
    



