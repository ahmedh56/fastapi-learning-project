from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, database, oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends (oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) #query to find if user already already voted on a specific post
    found_vote = vote_query.first()
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if post_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with id {vote.post_id}")

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": f"User {current_user.id} upvoted post {vote.post_id}"}
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"There is not post with id: {vote.post_id}")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": f"{vote.post_id} was deleted"}