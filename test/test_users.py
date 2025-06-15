from .utils import *
from fastapi import status
from routers.auth import get_current_user
from utils.db import get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    
    user = response.json()
    assert user["id"] == test_user.id
    assert user["username"] == test_user.username
    assert user["email"] == test_user.email
    assert user["role"] == test_user.role
    assert user["first_name"] == test_user.first_name
    assert user["last_name"] == test_user.last_name
    assert user["is_active"] == test_user.is_active
    assert user["phone_number"] == test_user.phone_number
    
def test_change_password_success(test_user):
    response = client.put("/users/change-password", json={
        "password": "test_password",
        "new_password": "test_new_password"
            
    })
    
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid(test_user):
    response = client.put("/users/change-password", json={
        "password": "wrong_password",
        "new_password": "test_new_password"
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}

def test_change_phone_number_success(test_user):
    response =client.put("/users/change-phone-number", json=(
        {
            "phone_number": "123-456-7890"
        }
    ))
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    
