from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from models import Base
from database import engine
from routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Mount static files directory before rendering templates
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=302)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)