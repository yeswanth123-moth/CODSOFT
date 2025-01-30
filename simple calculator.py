import tkinter as tk
from tkinter import messagebox
import math

def on_click(button_text):
    if button_text == '=':
        try:
            result = eval(entry.get())
            history.append(entry.get() + " = " + str(result))
            save_history()
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", "Invalid Expression")
    elif button_text == 'C':
        entry.delete(0, tk.END)
    elif button_text == '⌫':
        entry.delete(len(entry.get())-1, tk.END)
    elif button_text == '√':
        try:
            value = float(entry.get())
            result = math.sqrt(value)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input for Square Root")
    elif button_text == '^':
        entry.insert(tk.END, '**')
    elif button_text == '%':
        entry.insert(tk.END, '/100')
    elif button_text == 'History':
        show_history()
    else:
        entry.insert(tk.END, button_text)

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    
    history_listbox = tk.Listbox(history_window, width=40, height=10, font=("Arial", 12))
    history_listbox.pack(padx=10, pady=10)
    
    for item in history:
        history_listbox.insert(tk.END, item)
    
    clear_button = tk.Button(history_window, text="Clear History", font=("Arial", 12), command=clear_history, bg="black", fg="white")
    clear_button.pack(pady=5)

def clear_history():
    global history
    history = []
    save_history()
    messagebox.showinfo("History", "Calculation history cleared.")

def save_history():
    with open("history.txt", "w") as file:
        for item in history:
            file.write(item + "\n")

def load_history():
    try:
        with open("history.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def on_key(event):
    key = event.char
    if key in "0123456789+-*/.=()^%":
        entry.insert(tk.END, key)
    elif key == "\r":  # Enter key
        on_click('=')
    elif key == "\b":  # Backspace key
        on_click('⌫')

root = tk.Tk()
root.title("Advanced Calculator")
root.configure(bg="#222")
root.bind("<Key>", on_key)

entry = tk.Entry(root, width=18, font=("Arial", 20), bd=10, relief=tk.RIDGE, justify='right', bg="#f7f5f5", fg="green")
entry.grid(row=0, column=0, columnspan=4, pady=10)

buttons = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('C', '0', '.', '+'),
    ('⌫', '=', 'History', '√'),
    ('^', '%', '(', ')')
]

for r, row in enumerate(buttons, start=1):
    for c, text in enumerate(row):
        tk.Button(root, text=text, width=5, height=2, font=("Arial", 15), command=lambda t=text: on_click(t), bg="white", fg="green").grid(row=r, column=c, padx=5, pady=5)

history = load_history()

root.mainloop()

