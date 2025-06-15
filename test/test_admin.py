from fastapi import status
from routers.auth import get_current_user, get_db
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": test_todo.id,
            "title": test_todo.title,
            "description": test_todo.description,
            "priority": test_todo.priority,
            "completed": test_todo.completed,
            "owner_id": test_todo.owner_id,
            "created_at": test_todo.created_at.isoformat()
        }
    ]
    
def test_admin_delete_todo(test_todo):
    response = client.delete(f"/admin/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == "", "Response should be empty for successful deletion"
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None
    
def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}