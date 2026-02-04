from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import User, Todo
from auth import hash_password, verify_password, create_access_token
from database import load_todos, save_todos, update_todos, delete_todo, clear_todo, engine, get_db, Base, User

app = FastAPI(title="Clean To Do App")

Base.metadata.create_all(engine)

@app.post("/register")
async def register(username: str, password: str, db: Session = Depends(get_db)):
    
    existing = db.scalar(select(User).where(User.username == username))

    if existing:
        raise HTTPException(status_code=400, detail="Username taken")
    
    user = User(
        username=username, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username
        }

@app.post("login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == form.username))

    if not user or not verify_password(form.username,user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    
    token = create_access_token(user.username)

    return{"access_token": token, "token_type": "bearer"}

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def redirect_home():
    return RedirectResponse(url="/", status_code=303)



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    todos = load_todos()
    active_count = sum(1 for todo in todos if not todo['completed'])
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "todos": todos,
            "active_count": active_count
        }
    ) 

@app.post("/add")
def add_todo(task: str=Form(...)):
    if task.strip():
        save_todos(task.strip())
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle/{todo_id}")
def toggle_complete(todo_id:int):
    update_todos(todo_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{todo_id}")
def delete_selected_todo(todo_id:int):
    delete_todo(todo_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/clear_completed")
def clear_completed():
    clear_todo()
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/todos")
def get_todos():
    """Get all todos in JSON format"""
    return {"todos": load_todos()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
