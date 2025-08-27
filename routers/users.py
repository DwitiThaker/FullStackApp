from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import BaseModel, Field
from models import Todos, Users
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext  #type:ignore

router = APIRouter(prefix = '/users',
                   tags = ['users'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str 
    new_password: str = Field(min_length=6)

class UserPhoneNo(BaseModel):
    phone_number: str = Field(..., pattern="^[0-9]{10}$")  # must be 10 digits


@router.get("/", status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, db:db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('user_id')).first()




@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(user: user_dependency, db: db_dependency,
                    user_verification: UserVerification):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model.hased_password =  bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()




@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
def update_phone_no(
    user: user_dependency,
    db: db_dependency,
    phone_data: UserPhoneNo
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    # update phone
    user_model.phone_number = phone_data.new_phone_number
    db.commit()


