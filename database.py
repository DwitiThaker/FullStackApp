from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL =  'sqlite:///./todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


"""SQLALCHEMY_DATABASE_URL → Says where the database is and what type it is (here: a SQLite file named todosapp.db).

engine → The actual connection to the database; lets SQLAlchemy talk to it.

SessionLocal → A tool to make sessions (temporary “workspaces”) for doing database operations.

Base → The parent class you’ll use when creating database table models."""