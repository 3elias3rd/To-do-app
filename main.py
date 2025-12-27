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
