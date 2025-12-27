from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from pathlib import Path
import json

app = FastAPI(title="Clean To Do App")

templates = Jinja2Templates(directory="templates")

TODO_FILE = Path("todos.json")

def load_todos():
    """Load todos from JSON file"""
    if TODO_FILE.exists():
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Sava todos to JSON file"""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)    

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
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
        todos = load_todos()
        new_todo = {
            "id": len(todos) + 1,
            "task": task.strip(),
            "completed": False
        }
        todos.append(new_todo)
        save_todos(todos)
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle/{todo_id}")
async def toggle_complete(todo_id:int):
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break

@app.post("/delete/{todo_id}")
async def delete_todo(todo_id:int):
    todos = load_todos()
    todos = [todo for todo in todos if todo['id'] != todo_id]
    save_todos(todos)
    return RedirectResponse(url="/", status_code=303)

