from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values
import os

secrets = dotenv_values(".env")

DATABASE_URL = secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()