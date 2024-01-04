from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..models import Vote
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..oauth2 import get_current_user
from ..models import Vote, Post

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(user_vote: schemas.Vote, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == user_vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post not found!')
    vote_query = db.query(Vote).filter(Vote.user_id==user.id, Vote.post_id==post.id)
    vote = vote_query.first()
    if not vote:
        if user_vote.vote_dir:
            vote = Vote(user_id=user.id, post_id=user_vote.post_id)
            db.add(vote)
            db.commit()
            return {'message': 'successfully added vote'}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'you have not voted for this post!')
    else:
        if user_vote.vote_dir:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'you have already voted for this post!')
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {'message': 'successfully deleted vote'}
