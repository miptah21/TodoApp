from .utils import *
from routers.auth import get_current_user, authenticate_user, create_access_token, get_current_user, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException, status

app.dependency_overrides[get_current_user] = override_get_current_user

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    
    authenticated_user = authenticate_user(test_user.username, "test_password", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    
    non_existent_user = authenticate_user("non_existent", "test_password", db)
    assert non_existent_user is False
    
    wrong_password_user = authenticate_user(test_user.username, "wrong_password", db)
    assert wrong_password_user is False

def test_create_access_token(test_user):
    expires_delta = timedelta(minutes=30)
    token = create_access_token(
        username=test_user.username,
        user_id=test_user.id,
        user_role=test_user.role,
        expires_delta=expires_delta
    )
    
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
    assert decoded_token["sub"] == test_user.username
    assert decoded_token["user_id"] == test_user.id
    assert decoded_token["role"] == test_user.role
    assert "exp" in decoded_token

@pytest.mark.asyncio
async def test_get_current_user_valid_token(test_user):
    encode = {"sub": test_user.username, "user_id": test_user.id, "role": test_user.role}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    user = await get_current_user(token)
    assert user["username"] == test_user.username
    assert user["user_id"] == test_user.id
    assert user["role"] == test_user.role
    
@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"roke": "user"}  # Missing 'sub' and 'user_id'
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"