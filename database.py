import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

# Get the DB URL from an environment variable instead of hardcoding it
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please define it in your environment.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



"""SQLALCHEMY_DATABASE_URL → Says where the database is and what type it is (here: a SQLite file named todosapp.db).

engine → The actual connection to the database; lets SQLAlchemy talk to it.

SessionLocal → A tool to make sessions (temporary “workspaces”) for doing database operations.

Base → The parent class you’ll use when creating database table models."""