from sqlalchemy import text
from main import app
from utils.db import get_db # ❌ This causes the circular import
from routers.auth import get_current_user 
from fastapi import status
from models import Todos
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get(("/todos/"),)
    assert response.status_code == status.HTTP_200_OK, "Should return 200 OK for authenticated user"
    
    todos = response.json()
    assert len(todos) == 1, "Should return one todo item for the authenticated user"
    
    todo = todos[0]  # Take the first item since we are filtering by owner_id
    
    assert todo["title"] == test_todo.title, "Todo title should match"
    assert todo["description"] == test_todo.description, "Todo description should match"
    assert todo["priority"] == test_todo.priority, "Todo priority should match"
    assert todo["completed"] == test_todo.completed, "Todo completed status should match"
    assert todo["owner_id"] == test_todo.owner_id, "Todo owner ID should match"
    
    
def test_read_one(test_todo):
    response = client.get(f"/todos/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    
    todos = response.json()
    
    todo = todos[0] # Take the first item since we are filtering by owner_id

    assert todo["title"] == test_todo.title
    assert todo["description"] == test_todo.description
    assert todo["priority"] == test_todo.priority
    assert todo["completed"] == test_todo.completed
    assert todo["owner_id"] == test_todo.owner_id
    assert "created_at" in todo

    
def test_read_one_not_found():
    response = client.get("/todos/9999")  # Assuming this ID does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND
    print("Response JSON:", response.json())
    assert response.json() == {"detail": "Todos not found for this owner"}
    
def test_create_todo():
    request_data = {
        "title": "New Todo",
        "description": "This is a new todo item",
        "priority": 2,
        "completed": False
    }
    
    response = client.post("/todos/create_todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == response.json().get("id")).first()
    
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.completed == request_data.get("completed")
    
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
    
def test_update_todo(test_todo):
    update_data = {
        "title": "Updated Todo",
        "description": "This is an updated todo item",
        "priority": 1,
        "completed": True
    }
    
    response = client.put(f"/todos/update_todo/{test_todo.id}", json=update_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model.title == update_data.get("title")
    assert model.description == update_data.get("description")
    assert model.priority == update_data.get("priority")
    assert model.completed == update_data.get("completed")

def test_update_todo_not_found():
    update_data = {
        "title": "Updated Todo",
        "description": "This is an updated todo item",
        "priority": 1,
        "completed": True
    }
    
    response = client.put("/todos/update_todo/9999", json=update_data)  # Assuming this ID does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    
def test_delete_todo(test_todo):
    response = client.delete(f"/todos/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None, "Todo should be deleted from the database"
    
def test_delete_todo_not_found():
    response = client.delete("/todos/todo/9999")  # Assuming this ID does not exist
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
    
