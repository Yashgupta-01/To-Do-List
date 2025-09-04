import sqlite3
import os
from datetime import datetime

DB_FILE = 'todo_list.db'

def migrate_db():
    """Migrate the database to ensure all required columns exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if 'due_date' not in columns:
        cursor.execute('ALTER TABLE tasks ADD COLUMN due_date TEXT')
    
    if 'category' not in columns:
        cursor.execute('ALTER TABLE tasks ADD COLUMN category TEXT')
    
    conn.commit()
    conn.close()

def create_db():
    """Create the database and tasks table with all columns."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            due_date TEXT,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()
    migrate_db()

def add_task(description, due_date, category):
    """Add a new task with description, due date, and category."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (description, due_date, category) VALUES (?, ?, ?)', 
                  (description, due_date, category))
    conn.commit()
    conn.close()

def get_all_tasks(sort_by_due_date=False):
    """Retrieve all tasks, optionally sorted by due date."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = 'SELECT id, description, status, due_date, category FROM tasks'
    if sort_by_due_date:
        query += ' ORDER BY due_date ASC'
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_tasks_by_category(category):
    """Retrieve tasks filtered by category."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if category == "All":
        cursor.execute('SELECT id, description, status, due_date, category FROM tasks')
    else:
        cursor.execute('SELECT id, description, status, due_date, category FROM tasks WHERE category = ?', (category,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, new_description, new_due_date, new_category):
    """Update a task's description, due date, and category by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET description = ?, due_date = ?, category = ? WHERE id = ?', 
                  (new_description, new_due_date, new_category, task_id))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def complete_task(task_id):
    """Mark a task as completed by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status = "Completed" WHERE id = ?', (task_id,))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def delete_task(task_id):
    """Delete a task by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def validate_due_date(due_date):
    """Validate due date format (YYYY-MM-DD) and check if it's a valid date."""
    if not due_date:
        return True
    try:
        datetime.strptime(due_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False