from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from fastapi.testclient import TestClient
from models import Todos, Users
import pytest
from routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def override_get_current_user():
    return {"user_id": 1, "username": "test_user", "role": "admin"}

client = TestClient(app)

@pytest.fixture()
def test_todo():
    todo = Todos(
        title="Test Todo",
        description="This is a test todo item",
        priority=3,
        completed=False,
        owner_id=1
    )
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
        
@pytest.fixture()
def test_user():
    user = Users(
        username="test_user",
        email="g8TtF@example.com",
        hash_password=bcrypt_context.hash("test_password"),
        first_name="Test",
        last_name="User",
        role="admin",
        phone_number="1234567890",
        is_active=True
    )
    
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()