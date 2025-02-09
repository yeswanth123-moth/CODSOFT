import tkinter as tk 
from tkinter import messagebox
import random
import json

def determine_winner(user_choice, computer_choice):
    global user_score, computer_score, wins, losses, ties
    if user_choice == computer_choice:
        ties += 1
        return "It's a tie!"
    elif (user_choice == "🪨 Rock" and computer_choice == "✂️ Scissors") or \
         (user_choice == "✂️ Scissors" and computer_choice == "📄 Paper") or \
         (user_choice == "📄 Paper" and computer_choice == "🪨 Rock"):
        user_score += 1
        wins += 1
        return "You win!"
    else:
        computer_score += 1
        losses += 1
        return "You lose!"

def play_game(user_choice):
    computer_choice = random.choice(["🪨 Rock", "📄 Paper", "✂️ Scissors"])
    result = determine_winner(user_choice, computer_choice)
    result_label.config(text=f"Your choice: {user_choice}\nComputer's choice: {computer_choice}\n\n{result}")
    score_label.config(text=f"Your Score: {user_score}  |  Computer Score: {computer_score}")

def reset_scores():
    global user_score, computer_score, wins, losses, ties
    user_score = 0
    computer_score = 0
    wins = 0
    losses = 0
    ties = 0
    score_label.config(text=f"Your Score: {user_score}  |  Computer Score: {computer_score}")
    result_label.config(text="")

root = tk.Tk()
root.title("Rock-Paper-Scissors Game ✊📄✂️")
root.geometry("400x400")

user_score = 0
computer_score = 0
wins = 0
losses = 0
ties = 0

instructions = tk.Label(root, text="Choose Rock, Paper, or Scissors:", font=("Arial", 14))
instructions.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

rock_button = tk.Button(button_frame, text="🪨 Rock", font=("Arial", 12), width=10, command=lambda: play_game("🪨 Rock"))
rock_button.grid(row=0, column=0, padx=10)

paper_button = tk.Button(button_frame, text="📄 Paper", font=("Arial", 12), width=10, command=lambda: play_game("📄 Paper"))
paper_button.grid(row=0, column=1, padx=10)

scissors_button = tk.Button(button_frame, text="✂️ Scissors", font=("Arial", 12), width=10, command=lambda: play_game("✂️ Scissors"))
scissors_button.grid(row=0, column=2, padx=10)

result_label = tk.Label(root, text="", font=("Arial", 12), wraplength=300)
result_label.pack(pady=20)

score_label = tk.Label(root, text=f"Your Score: {user_score}  |  Computer Score: {computer_score}", font=("Arial", 12))
score_label.pack(pady=10)

reset_button = tk.Button(root, text="Reset Scores", font=("Arial", 12), width=15, command=reset_scores)
reset_button.pack(pady=10)

root.mainloop()