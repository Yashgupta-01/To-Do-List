import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import re
from db_handler import get_all_tasks, add_task, update_task, complete_task, delete_task, validate_due_date, get_tasks_by_category

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List App")
        self.root.geometry("700x500")
        
        # Apply modern theme (comment out if ttkthemes not installed)
        try:
            self.root.set_theme('arc')
        except:
            pass  # Fallback to default Tkinter theme

        # Categories for dropdown
        self.categories = ["Work", "Personal", "Urgent", "Other"]

        # Input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10, padx=10)

        tk.Label(self.input_frame, text="Description:").grid(row=0, column=0, sticky="e", padx=5)
        self.task_entry = tk.Entry(self.input_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5)
        # Register validation function
        vcmd = (self.root.register(self.validate_due_date_entry), '%P')
        self.due_date_entry = tk.Entry(self.input_frame, width=20, validate="key", validatecommand=vcmd)
        self.due_date_entry.grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(self.input_frame, text="Category:").grid(row=2, column=0, sticky="e", padx=5)
        self.category_var = tk.StringVar(value=self.categories[0])
        self.category_menu = ttk.Combobox(self.input_frame, textvariable=self.category_var, 
                                       values=self.categories, state="readonly", width=20)
        self.category_menu.grid(row=2, column=1, sticky="w", padx=5)

        self.add_button = ttk.Button(self.input_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Task list
        self.tree = ttk.Treeview(root, columns=("ID", "Description", "Status", "Due Date", "Category"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Category", text="Category")
        self.tree.column("ID", width=50)
        self.tree.column("Description", width=300)
        self.tree.column("Status", width=100)
        self.tree.column("Due Date", width=100)
        self.tree.column("Category", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tag configuration for status colors
        self.tree.tag_configure("Completed", foreground="green")
        self.tree.tag_configure("Pending", foreground="black")

        # Action buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.update_button = ttk.Button(self.button_frame, text="Update Selected", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.complete_button = ttk.Button(self.button_frame, text="Complete Selected", command=self.complete_task)
        self.complete_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Selected", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.sort_button = ttk.Button(self.button_frame, text="Sort by Due Date", command=self.sort_by_due_date)
        self.sort_button.pack(side=tk.LEFT, padx=5)

        # Filter by category
        tk.Label(self.button_frame, text="Filter by Category:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value="All")
        self.filter_menu = ttk.Combobox(self.button_frame, textvariable=self.filter_var, 
                                      values=["All"] + self.categories, state="readonly", width=15)
        self.filter_menu.pack(side=tk.LEFT, padx=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.filter_tasks)

        # Load initial tasks
        self.load_tasks()

    def validate_due_date_entry(self, new_value):
        """Validate due date input in real-time to ensure YYYY-MM-DD format or empty."""
        if not new_value:
            return True  # Allow empty input
        # Allow partial valid date formats (e.g., '2025', '2025-', '2025-09', '2025-09-')
        if re.match(r'^\d{0,4}(-\d{0,2}(-\d{0,2})?)?$', new_value):
            return True
        return False

    def load_tasks(self, sort_by_due_date=False):
        """Load tasks into the Treeview, optionally sorted."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = get_all_tasks(sort_by_due_date)
        for task in tasks:
            tag = "Completed" if task[2] == "Completed" else "Pending"
            self.tree.insert("", tk.END, values=task, tags=(tag,))

    def filter_tasks(self, event=None):
        """Filter tasks by selected category."""
        category = self.filter_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = get_tasks_by_category(category)
        for task in tasks:
            tag = "Completed" if task[2] == "Completed" else "Pending"
            self.tree.insert("", tk.END, values=task, tags=(tag,))

    def add_task(self):
        """Add a new task from input fields."""
        description = self.task_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        category = self.category_var.get()

        if not description:
            messagebox.showwarning("Input Error", "Task description cannot be empty.")
            return
        if not validate_due_date(due_date):
            messagebox.showwarning("Input Error", "Invalid due date format. Use YYYY-MM-DD or leave empty.")
            return

        add_task(description, due_date, category)
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.load_tasks()

    def get_selected_task(self):
        """Get the values of the selected task."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "No task selected.")
            return None
        item = self.tree.item(selected[0])
        return item["values"]

    def update_task(self):
        """Update the selected task's description, due date, and category."""
        task = self.get_selected_task()
        if task is None:
            return
        task_id = task[0]
        new_description = self.task_entry.get().strip()
        new_due_date = self.due_date_entry.get().strip()
        new_category = self.category_var.get()

        if not new_description:
            messagebox.showwarning("Input Error", "New description cannot be empty.")
            return
        if not validate_due_date(new_due_date):
            messagebox.showwarning("Input Error", "Invalid due date format. Use YYYY-MM-DD or leave empty.")
            return

        if update_task(task_id, new_description, new_due_date, new_category):
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showerror("Update Error", "Task not found.")

    def complete_task(self):
        """Mark the selected task as completed."""
        task = self.get_selected_task()
        if task is None:
            return
        if complete_task(task[0]):
            self.load_tasks()
        else:
            messagebox.showerror("Complete Error", "Task not found.")

    def delete_task(self):
        """Delete the selected task."""
        task = self.get_selected_task()
        if task is None:
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            if delete_task(task[0]):
                self.load_tasks()
            else:
                messagebox.showerror("Delete Error", "Task not found.")

    def sort_by_due_date(self):
        """Sort tasks by due date."""
        self.load_tasks(sort_by_due_date=True)