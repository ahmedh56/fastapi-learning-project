from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostVote]) #gets all posts
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # post = cursor.fetchall()
    # post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code=201, response_model = schemas.PostResponse) #creates a new post
def create_post(newPost: schemas.PostCreate, db: Session = Depends(get_db),  current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (newPost.title, newPost.content, newPost.published))
    # newUserPost = cursor.fetchone()
    # conn.commit()
    
    newUserPost = models.Post(owner_id = current_user.id, **newPost.model_dump())
    if newUserPost.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")    
    db.add(newUserPost)
    db.commit()
    db.refresh(newUserPost)
    return newUserPost

@router.get("/{id}", response_model=schemas.PostVote) #gets a post by id
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # postByID = cursor.fetchone()
    # postByID = db.query(models.Post).filter(models.Post.id == id).first()

    post_by_id = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post_by_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with id: " + str(id))

    return post_by_id 

@router.put("/{id}", status_code=200, response_model=schemas.PostResponse) #updates* a existing post by id, dif from post which creates a 'new' post
def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # post_index = id
    
    # else:
    #     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    #     updatedPostByID = cursor.fetchone()
    #     conn.commit()
    print(current_user)
    postFromDB = db.query(models.Post).filter(models.Post.id == id)

    updatedPostByID = postFromDB.first()

    if updatedPostByID is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with id: " + str(id))
    
    if updatedPostByID.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    postFromDB.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(updatedPostByID)

    return updatedPostByID
    
@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # postToDelete = cursor.fetchone()
    # conn.commit()
    print(current_user)
    postToDelete_query = db.query(models.Post).filter(models.Post.id == id)

    postToDelete = postToDelete_query.first()
    
    if postToDelete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found with id: " + str(id))

    if postToDelete.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    postToDelete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)