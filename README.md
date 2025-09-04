To-Do List Web Application
A simple, modern, and responsive To-Do List web application built with Flask, SQLite, and Bootstrap. Manage tasks with descriptions, due dates, categories, and statuses, with a clean UI and real-time due date validation.
Features

Task Management: Add, view, update, complete, and delete tasks.
Due Date Validation: Restricts due date input to YYYY-MM-DD format (or empty) using a browser-native date picker and JavaScript validation.
Categories: Organize tasks into categories (Work, Personal, Urgent, Other).
Sorting and Filtering: Sort tasks by due date or filter by category.
Responsive UI: Built with Bootstrap 5 for a modern, mobile-friendly interface.
Persistent Storage: Uses SQLite to store tasks, preserving data between sessions.
Visual Feedback: Color-coded task statuses (Pending: orange, Completed: green) and flash messages for user actions.

Project Structure
todo_gui_app/
├── main.py              # Flask app entry point and routes
├── db_handler.py        # SQLite database operations
├── requirements.txt     # Dependencies (Flask)
├── README.md            # Project documentation
├── templates/
│   ├── index.html       # Main page with task list and form
│   └── update_task.html # Page for updating tasks
├── static/
│   ├── css/
│   │   └── styles.css   # Custom CSS styles
│   └── js/
│       └── scripts.js   # JavaScript for client-side validation

Prerequisites

Python 3.8 or higher: Install from python.org.
Git: For cloning the repository (optional).
VS Code: Recommended for development, with the Python extension installed.

Installation

Clone the Repository (or use your existing project folder):
git clone https://github.com/your-username/todo_gui_app.git
cd todo_gui_app

Replace your-username with your GitHub username, or use D:\To Do List App if already set up.

Set Up a Virtual Environment (optional but recommended):
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux


Install Dependencies:
pip install -r requirements.txt

This installs Flask. No other dependencies are required as Bootstrap is included via CDN.

Verify Folder Structure:Ensure templates/ contains index.html and update_task.html, and static/ contains css/styles.css and js/scripts.js.


Running the App

Start the Flask Server:
python main.py

The app will run on http://127.0.0.1:5000.

Access the App:Open a browser and navigate to http://127.0.0.1:5000.

Stop the Server:Press Ctrl+C in the terminal.


Usage

Add a Task:
Enter a description (required).
Select a due date using the date picker (YYYY-MM-DD format) or leave empty.
Choose a category (Work, Personal, Urgent, Other).
Click "Add Task".


View Tasks:
Tasks appear in a table with ID, Description, Status, Due Date, and Category.
Status is color-coded: Pending (orange), Completed (green).


Update a Task:
Click "Update" to open a pre-filled form, edit fields, and submit.


Complete/Delete a Task:
Click "Complete" to mark as completed or "Delete" (with confirmation).


Sort and Filter:
Use the "Sort by Due Date" button to order tasks chronologically.
Select a category from the filter dropdown to show specific tasks.



Example:

Add a task: Description: "Buy groceries", Due Date: 2025-09-10, Category: Personal.
Update it to: "Buy groceries and milk".
Filter by "Personal" to see only Personal tasks.

Due Date Validation

Client-Side: The <input type="date"> field provides a calendar picker, ensuring YYYY-MM-DD output. JavaScript (scripts.js) validates manual input.
Server-Side: The validate_due_date function in db_handler.py ensures only valid dates or empty inputs are saved.
Behavior: Invalid dates (e.g., 2025-13-10) trigger an error message, and the date picker prevents incorrect formats.

Troubleshooting

TemplateNotFound Error:
Ensure templates/index.html and templates/update_task.html exist in D:\To Do List App\templates.
Verify file names are exact (case-sensitive on some systems).


Static Files Not Loading:
Check static/css/styles.css and static/js/scripts.js exist.
Inspect browser console (F12) for errors.


Database Issues:
If you see no such column: due_date, delete todo_list.db or ensure db_handler.py includes migrate_db.
Verify the database schema:import sqlite3
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(tasks)")
print(cursor.fetchall())
conn.close()




Flask Not Found:
Run pip install flask if you see No module named flask.



Development

VS Code Setup:
Open D:\To Do List App in VS Code.
Install the Python extension for IntelliSense and debugging.
Run main.py via F5 or the


