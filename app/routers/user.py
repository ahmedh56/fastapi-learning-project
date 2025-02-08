from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/", status_code=201, response_model=schemas.UserResponse) 
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    newUser = models.User(**user.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.get("/{id}", )
def get_user(id:int, db: Session = Depends(get_db), response_model=schemas.UserResponse):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no user with id:" + str(id))

    return user