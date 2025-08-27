#represent the difference between two datetime objects.
#By using SessionLocal, you ensure that each interaction with the database is treated as a separate, isolated unit of work, helping keep your application's data consistent and reliable.
#access the JSON Web Token (JWT) functionality

from fastapi import APIRouter, Depends
from starlette import status 
from typing import Annotated
from pydantic import BaseModel
from database import SessionLocal
from jose import jwt # type: ignore
from datetime import datetime, timedelta, timezone
from models import Users
from sqlalchemy.orm import Session
from passlib.context import CryptContext # type: ignore
from fastapi.security import OAuth2PasswordRequestForm

fastapi = APIRouter()

import secrets
print(secrets.token_hex(32))

SECRET_KEY = 'd6fbeb3609b1e0a0d1a1cf449bd0ca6b396111378fe84ad06a5d34ae8a2c8c04'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: str
    role: str

class Token(BaseModel):
    access_token : str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

