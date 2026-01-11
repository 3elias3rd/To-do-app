from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from pathlib import Path
import json
from database import load_todos, save_todos, clear_todo, delete_todo, update_todos

app = FastAPI(title="Clean To Do App")

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

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
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            new_status = not todo['completed']
            update_todos(todo_id, new_status)
            break
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

