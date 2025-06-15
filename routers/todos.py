from models import Todos
from database import  SessionLocal
from fastapi import Depends, HTTPException, Path, APIRouter, Request
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import RedirectResponse
from .auth import get_current_user
from utils.db import get_db, db_dependency, user_dependency
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/todos", tags=["todos"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequestModel(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="Title of the todo item")
    description: str = Field(min_length=1, max_length=1000, description="Description of the todo item")
    priority: int = Field(ge=1, le=5, description="Priority of the todo item (1-5)")
    completed: bool = Field(default=False, description="Completion status of the todo item")
    
    class Config:
        from_attributes: True
        json_schema_extra = {
            "example": {
                "title": "Sample Todo",
                "description": "This is a sample todo item",
                "priority": 3,
                "completed": False,
            }
        }

templates = Jinja2Templates(directory="templates")

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### Pages ###
@router.get("/todo-page")
async def todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
    
    except:
        return redirect_to_login()

@router.get("/add-todo-page")
async def add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if user is None:
            return redirect_to_login()
        
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        
        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})
    except:
        return redirect_to_login()

### Endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

@router.get("/{owner_id}", status_code=status.HTTP_200_OK)
async def read_todos_by_owner(db:db_dependency, owner_id: Annotated[int, Path(title="Owner ID", ge=0)]):
    todos = db.query(Todos).filter(Todos.owner_id == owner_id).all()
    # Check if the todos exist
    if not todos:
        raise HTTPException(status_code=404, detail="Todos not found for this owner")
    return todos

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(title="Todo ID", ge=0)]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    # Check if the todo item existsS
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo: TodoRequestModel):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    todos_model = Todos(**todo.model_dump(), owner_id=user.get("id"))
    db.add(todos_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(title='Todo ID', gt=0)], todo: TodoRequestModel):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    todos = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    todos.title = todo.title
    todos.description = todo.description
    todos.priority = todo.priority
    todos.completed = todo.completed
    db.commit()
    return {"message": "Todo updated", "todo_updated": todos}

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(tittle='Todo ID', gt=0)]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted", "todos_deleted": todo}