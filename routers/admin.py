from models import Todos, Users
from database import SessionLocal
from fastapi import Depends, HTTPException, Path, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from .auth import get_current_user
from utils.db import get_db, db_dependency, user_dependency


router = APIRouter(prefix="/admin", tags=["admin"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_todos(
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )
    
    return db.query(Users).all()

@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all_todos(
    db: db_dependency,
    user: user_dependency
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )
    
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: Annotated[int, Path(title="Todo ID", ge=0)]
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this todo."
        )
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted successfully"}