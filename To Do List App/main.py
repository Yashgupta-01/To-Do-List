from flask import Flask, render_template, request, redirect, url_for, flash
from db_handler import create_db, add_task, get_all_tasks, update_task, complete_task, delete_task, get_tasks_by_category, validate_due_date
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

DB_FILE = 'todo_list.db'

@app.route('/', methods=['GET', 'POST'])
def index():
    sort_by_due_date = request.args.get('sort', 'false') == 'true'
    category_filter = request.args.get('category', 'All')
    
    if request.method == 'POST':
        description = request.form['description'].strip()
        due_date = request.form['due_date'].strip()
        category = request.form['category']
        
        if not description:
            flash('Task description cannot be empty.', 'error')
        elif not validate_due_date(due_date):
            flash('Invalid due date format. Use YYYY-MM-DD or leave empty.', 'error')
        else:
            add_task(description, due_date, category)
            flash('Task added successfully!', 'success')
            return redirect(url_for('index'))
    
    tasks = get_tasks_by_category(category_filter) if category_filter != 'All' else get_all_tasks(sort_by_due_date)
    return render_template('index.html', tasks=tasks, category_filter=category_filter, categories=["Work", "Personal", "Urgent", "Other"])

@app.route('/complete/<int:task_id>')
def complete(task_id):
    if complete_task(task_id):
        flash('Task marked as completed!', 'success')
    else:
        flash('Task not found.', 'error')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if delete_task(task_id):
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found.', 'error')
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    tasks = get_all_tasks()
    task = next((t for t in tasks if t[0] == task_id), None)
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_description = request.form['description'].strip()
        new_due_date = request.form['due_date'].strip()
        new_category = request.form['category']
        
        if not new_description:
            flash('Task description cannot be empty.', 'error')
        elif not validate_due_date(new_due_date):
            flash('Invalid due date format. Use YYYY-MM-DD or leave empty.', 'error')
        else:
            if update_task(task_id, new_description, new_due_date, new_category):
                flash('Task updated successfully!', 'success')
            else:
                flash('Task not found.', 'error')
            return redirect(url_for('index'))
    
    return render_template('update_task.html', task=task, categories=["Work", "Personal", "Urgent", "Other"])

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        create_db()
    else:
        create_db()
    app.run(debug=True)