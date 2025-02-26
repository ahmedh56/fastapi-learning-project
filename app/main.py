from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post,user, auth, vote




# models.Base.metadata.create_all(bind=engine) - command that tells SQLAlchemy to create the tables in the database, now using alembic to manage the database schema

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI to update posts db in PostgreSQL server"}



