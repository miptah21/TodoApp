from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from pytest import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi.templating import Jinja2Templates
# from utils.db import get_db # ❌ This causes the circular import

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "fa12f3bf09b233d2611c0cea230501393a358401d14b8085587b6610a22cb693"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class UserRequestModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: Annotated[str, None] = None  # Optional field
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "lH6eD@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123",
                "role": "user",
                "phone_number": "123-456-7890"  # Optional field
            }
        }
    
class Token(BaseModel):
    access_token: str
    token_type: str
        
db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="templates")

### Pages ###
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

### Endpoints ###

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hash_password):
        return False
    return user

def create_access_token(username: str, user_id: int, user_role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    # Check cookie token first
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"})
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    
        
@router.post("/", status_code=status.HTTP_201_CREATED)
async def created_user(db: db_dependency, create_request_user: UserRequestModel):
    create_user_model = Users(
        username=create_request_user.username,
        email=create_request_user.email,
        first_name=create_request_user.first_name,
        last_name=create_request_user.last_name,
        hash_password=bcrypt_context.hash(create_request_user.password),
        role=create_request_user.role,
        is_active=True,
        phone_number=create_request_user.phone_number  # Optional field
    )
    
    db.add(create_user_model)
    db.commit()
    
    return {"message": "User created successfully", "user": create_user_model}

@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    
    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=30)
    )
    
    return {"access_token": token, "token_type": "bearer"}