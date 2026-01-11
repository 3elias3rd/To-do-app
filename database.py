import psycopg2
from psycopg2.extras import RealDictCursor
from password import password

class Database:
    def __init__(self):
        self.conn=psycopg2.connect(
            host="localhost",
            database="todo_app_db",
            user="postgres",
            password=password
        )
    
    def get_cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)
    
    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.conn.close()
    
def load_todos():
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("SELECT * FROM todos ORDER BY id;")
    todos = cursor.fetchall()
    cursor.close()
    db.close()

    return [dict(todo) for todo in todos]

def save_todos(task, completed=False):
    db = Database()
    cursor = db.get_cursor()
    cursor.execute("INSERT INTO todos (task, completed) VALUES(%s, %s) Returning id;", (task, completed))

    new_id = cursor.fetchone()['id']
    db.commit()
    cursor.close()
    db.close()

def update_todos(todo_id, completed):
    db = Database()
    cursor = db.get_cursor()
    
    cursor.execute("UPDATE todos SET completed=%s WHERE id=%s;", (completed, todo_id))

    db.commit()
    cursor.close()
    db.close()

def delete_todo(todo_id):
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("DELETE FROM todos WHERE id=%s;", (todo_id,))

    db.commit()
    cursor.close()
    db.close()

def clear_todo():
    db = Database()
    cursor = db.get_cursor()

    cursor.execute("DELETE FROM todos WHERE completed=True;")

    db.commit()
    cursor.close()
    db.close()