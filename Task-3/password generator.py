import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import pyperclip
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def calculate_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    categories = sum([has_upper, has_lower, has_digit, has_special])

    if length >= 12 and categories == 4:
        return 'Strong'
    elif length >= 8 and categories >= 3:
        return 'Medium'
    else:
        return 'Weak'

def update_strength_meter(strength):
    if strength == 'Strong':
        strength_var.set(100)
        strength_label.config(text='Strength: Strong', foreground='green')
    elif strength == 'Medium':
        strength_var.set(60)
        strength_label.config(text='Strength: Medium', foreground='orange')
    else:
        strength_var.set(30)
        strength_label.config(text='Strength: Weak', foreground='red')

def generate_pronounceable_password(length):
    vowels = 'aeiou'
    consonants = ''.join(set(string.ascii_lowercase) - set(vowels))
    password = []

    for i in range(length):
        if i % 2 == 0:
            password.append(random.choice(consonants))
        else:
            password.append(random.choice(vowels))

    return ''.join(password)

def generate_password():
    length = length_var.get()
    include_uppercase = uppercase_var.get()
    include_digits = digits_var.get()
    include_special = special_var.get()
    pronounceable = pronounceable_var.get()

    if length <= 0:
        messagebox.showerror("Invalid Input", "Password length must be a positive integer.")
        return

    if pronounceable:
        # Generate a pronounceable password
        password = generate_pronounceable_password(length)
    else:
        # Generate a random password
        character_pool = string.ascii_lowercase
        if include_uppercase:
            character_pool += string.ascii_uppercase
        if include_digits:
            character_pool += string.digits
        if include_special:
            character_pool += string.punctuation

        if not character_pool:
            messagebox.showerror("Invalid Selection", "Please select at least one character type.")
            return

        password = ''.join(random.choice(character_pool) for _ in range(length))

    # Display the generated password
    result_var.set(password)
    password_history.append(password)
    history_listbox.insert(tk.END, password)

    # Update password strength
    strength = calculate_strength(password)
    update_strength_meter(strength)

    # Speak the generated password
    speak(f"The generated password is: {password}")

def copy_to_clipboard():
    password = result_var.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")
    else:
        messagebox.showwarning("No Password", "No password to copy.")

def save_passwords_to_file():
    if password_history:
        with open("passwords.txt", "w") as file:
            for pwd in password_history:
                file.write(pwd + "\n")
        messagebox.showinfo("Saved", "Passwords saved to passwords.txt.")
    else:
        messagebox.showwarning("No Passwords", "No passwords to save.")

# Initialize the main window
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("500x500")
root.resizable(False, False)

# Variables to store user input
length_var = tk.IntVar(value=12)
uppercase_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)
pronounceable_var = tk.BooleanVar(value=False)
result_var = tk.StringVar()
strength_var = tk.IntVar(value=0)
password_history = []

# GUI Elements
tk.Label(root, text="Password Length:").pack(pady=10)
tk.Spinbox(root, from_=1, to=100, textvariable=length_var, width=5).pack()

tk.Checkbutton(root, text="Include Uppercase Letters", variable=uppercase_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Digits", variable=digits_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Special Characters", variable=special_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Generate Pronounceable Password", variable=pronounceable_var).pack(anchor='w', padx=20)

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=20)

tk.Label(root, text="Generated Password:").pack(pady=5)
tk.Entry(root, textvariable=result_var, width=50, state='readonly').pack()

strength_label = tk.Label(root, text="Strength: N/A")
strength_label.pack(pady=5)
ttk.Progressbar(root, length=200, variable=strength_var, maximum=100).pack(pady=5)

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=10)
tk.Button(root, text="Save Passwords to File", command=save_passwords_to_file).pack(pady=5)

tk.Label(root, text="Password History:").pack(pady=5)
history_listbox = tk.Listbox(root, width=50, height=5)
history_listbox.pack(pady=5)

# Start the GUI event loop
root.mainloop()