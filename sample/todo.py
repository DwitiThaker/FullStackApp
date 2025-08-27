from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from .auth import get_current_user
from database import SessionLocal
from starlette import status
from typing import Annotated, Dict
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


class Todorequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=10)
    priority: int = Field(gt=0, lt=10)
    complete: bool


# ~ CRUDE ROUTE LOGIC

#! a) Read All Todos  b) Read One Todo   c) Create Todo  d) Update Todo  e) Delete Todo


@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db:db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()
    



@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db:db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('user_id')).first()
    
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')




@router.post("/todos", status_code=status.HTTP_201_CREATED)
def craete_todo(user: user_dependency, db:db_dependency,  todo_request:Todorequest):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = Todos(**todo_request.dict(), owner_id = user.get('user_id'))
    db.add(todo_model)
    db.commit()



@router.put("/todos", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependency, 
                db:db_dependency,
                todo_request: Todorequest,
                todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
            .filter(Todos.owner_id == user.get('user_id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)   
    db.commit()




@router.delete("/todos", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db:db_dependency, todo_id : int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('user_id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('user_id')).delete()
    
    db.commit()