from models import Users
from database import SessionLocal
from fastapi import Depends, HTTPException, Path, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext
from utils.db import get_db, db_dependency, user_dependency

router = APIRouter(prefix="/users", tags=["users"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserResponseModel(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    phone_number: str | None = None  # Optional phone number field
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "lH6eD@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": "user",
                "is_active": True,
                "phone_number": "123-456-7890"  # Optional phone number
            }
        }
        
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "password": "password",
                "new_password": "new_password"
            }
        }

@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponseModel)
async def read_user(
    db: db_dependency,
    user: user_dependency
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    return db.query(Users).filter(Users.id == user.get("id")).first()

@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_passsword(
    user: user_dependency,
    db: db_dependency,
    user_verification: UserVerification
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error on password change"
        )
    
    user_model.hash_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    return {"message": "Password updated successfully"}
    
    
@router.put("/change-phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency,
    db: db_dependency,
    phone_number: Annotated[str, None] = None
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    return {"message": "Phone number updated successfully"}
