from routers.todos import get_db, get_current_user  # Import from todos router
from fastapi import status
from .utils import *


# Set up dependency overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    
    response_data = response.json()
    assert len(response_data) == 1
    
    todo_item = response_data[0]
    assert todo_item['complete'] == False
    assert todo_item['title'] == 'Learn to code'
    assert todo_item['description'] == 'need to learn every day'
    assert todo_item['priority'] == 5
    assert todo_item['owner_id'] == 1

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todos/1")
    assert response.status_code == status.HTTP_200_OK
    
    todo_item = response.json()

    assert todo_item['complete'] == False
    assert todo_item['title'] == 'Learn to code'
    assert todo_item['description'] == 'need to learn every day'
    assert todo_item['priority'] == 5
    assert todo_item['owner_id'] == 1


def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todos/todos/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}


def test_create_todo():
    todo_payload = {
        "title": "Learn to code",
        "description": "need to learn every day",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todos/todos", json=todo_payload)
    print("DEBUG RESPONSE:", response.json())   
    assert response.status_code == status.HTTP_201_CREATED

    todo_data = response.json()
    assert todo_data['title'] == 'Learn to code'


def test_update_todo(test_todo):
    request_data = {
        "title": "Learn to dsa",
        "description": "need to learn efor test",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todos/todos/1", json=request_data)
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Learn to dsa"


