import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import threading

class ToDoList:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.init_gui()
        self.start_due_date_checker()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                title TEXT NOT NULL,
                                description TEXT,
                                category TEXT,
                                priority TEXT,
                                due_date TEXT,
                                status TEXT DEFAULT 'Pending')''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                                id INTEGER PRIMARY KEY,
                                task_id INTEGER,
                                title TEXT,
                                action TEXT,
                                timestamp TEXT)''')
        self.conn.commit()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        category = self.category_entry.get()
        priority = self.priority_entry.get()
        due_date = self.calendar.get_date()
        
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
        
        self.cursor.execute('''INSERT INTO tasks (title, description, category, priority, due_date, status) 
                               VALUES (?, ?, ?, ?, ?, 'Pending')''',
                            (title, description, category, priority, due_date))
        task_id = self.cursor.lastrowid
        self.log_history(task_id, title, "Added")
        self.conn.commit()
        self.view_tasks()
        
    def view_tasks(self):
        self.listbox.delete(0, tk.END)
        self.cursor.execute("SELECT id, title, status FROM tasks")
        tasks = self.cursor.fetchall()
        for task in tasks:
            self.listbox.insert(tk.END, f"{task[0]} - {task[1]} ({task[2]})")
    
    def mark_done(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No task selected")
            return
        task_id = int(self.listbox.get(selected).split(" - ")[0])
        title = self.listbox.get(selected).split(" - ")[1].split(" (")[0]
        self.cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
        self.log_history(task_id, title, "Completed")
        self.conn.commit()
        self.view_tasks()

    def delete_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No task selected")
            return
        task_id = int(self.listbox.get(selected).split(" - ")[0])
        title = self.listbox.get(selected).split(" - ")[1].split(" (")[0]
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.log_history(task_id, title, "Deleted")
        self.conn.commit()
        self.view_tasks()
    
    def log_history(self, task_id, title, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''INSERT INTO history (task_id, title, action, timestamp) 
                               VALUES (?, ?, ?, ?)''', (task_id, title, action, timestamp))
        self.conn.commit()
    
    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Task History")
        history_listbox = tk.Listbox(history_window)
        history_listbox.pack()
        self.cursor.execute("SELECT title, action, timestamp FROM history")
        history_entries = self.cursor.fetchall()
        for entry in history_entries:
            history_listbox.insert(tk.END, f"{entry[0]} - {entry[1]} at {entry[2]}")
    
    def check_due_dates(self):
        while True:
            today = datetime.date.today().strftime("%Y-%m-%d")
            self.cursor.execute("SELECT title FROM tasks WHERE due_date = ? AND status = 'Pending'", (today,))
            due_tasks = self.cursor.fetchall()
            if due_tasks:
                messagebox.showwarning("Due Task Reminder", f"You have tasks due today: {', '.join(task[0] for task in due_tasks)}")
            self.conn.commit()
            threading.Event().wait(86400)  # Check every 24 hours
    
    def start_due_date_checker(self):
        thread = threading.Thread(target=self.check_due_dates, daemon=True)
        thread.start()

    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("To-Do List")
        self.root.configure(bg="#d3d3d3")

        tk.Label(self.root, text="Title:", bg="#d3d3d3").pack()
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        tk.Label(self.root, text="Description:", bg="#d3d3d3").pack()
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.pack()

        tk.Label(self.root, text="Category:", bg="#d3d3d3").pack()
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        tk.Label(self.root, text="Priority:", bg="#d3d3d3").pack()
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.pack()

        tk.Label(self.root, text="Due Date:", bg="#d3d3d3").pack()
        self.calendar = Calendar(self.root)
        self.calendar.pack()

        tk.Button(self.root, text="Add Task", command=self.add_task).pack()
        tk.Button(self.root, text="Mark Done", command=self.mark_done).pack()
        tk.Button(self.root, text="Delete Task", command=self.delete_task).pack()
        tk.Button(self.root, text="View History", command=self.view_history).pack()

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()
        self.view_tasks()

        self.root.mainloop()

if __name__ == "__main__":
    ToDoList()