from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Session
from sqlalchemy import create_engine, select, delete
from password import password

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todos"
    id:  Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    completed: Mapped[bool]

database_URL = (f"postgresql://postgres:{password}@localhost:5432/todo_app_db")

engine = create_engine(database_URL, echo=True)

def load_todos():
    with Session(engine) as session:
        stmt = select(Todo).order_by(Todo.id)
        result = session.execute(stmt)
       
        return [
            {
                "id": todo.id,
                "task": todo.task,
                "completed":todo.completed,
            } 
            for todo in result.scalars()]

def save_todos(task, completed=False):
    with Session(engine) as session:
        todo = Todo(task=task, completed=completed)
        session.add(todo)
        session.commit()
        return(todo.id)
    
def update_todos(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            return None

        todo.completed = not todo.completed
        session.commit()
        session.refresh(todo)

        return {
            "id": todo.id,
            "task": todo.task,
            "completed": todo.completed,
        }   

def delete_todo(todo_id):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if todo == None:
            return None
        
        session.delete(todo)
        session.commit()

    return True

def clear_todo():
    with Session(engine) as session:
        stmt = delete(Todo).where(Todo.completed == True)
        session.execute(stmt)
        session.commit()
    



