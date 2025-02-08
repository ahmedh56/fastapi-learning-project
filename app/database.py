from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
import psycopg
# from psycopg.rows import dict_row

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# try:
#     conn = psycopg.connect(dbname="fastapi", user="postgres", password="AeroData56!", host="localhost", row_factory=psycopg.rows.dict_row)
#     cursor = conn.cursor()
#     print("Connected to the database")
# except Exception as error:
#     print("Error connecting to the database: " + str(error))