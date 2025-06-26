import tkinter as tk
from tkinter import ttk
import random
import time

def create_time():
    return time.time()

def calculate_difference(start, end):
    return end - start

def generate_random(max_num):
    return random.randint(0, max_num)

class GuessingGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("🎮 Guessing Game")
        master.geometry("400x350")
        master.configure(bg="#1e1e2f")

        # Setup style
        style = ttk.Style()
        style.theme_use('clam')  # More modern than 'default'
        style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 11), padding=8)
        style.configure("TEntry", padding=6, font=("Segoe UI", 11))

        self.number_to_guess = generate_random(10)
        self.start_time = create_time()
        self.attempts_left = 3

        self.label = ttk.Label(master, text="Guess a number between 0 and 10:")
        self.label.pack(pady=12)

        self.entry = ttk.Entry(master, width=18)
        self.entry.pack(pady=6)
        self.entry.focus()

        self.attempts_label = ttk.Label(master, text=f"Attempts left: {self.attempts_left}")
        self.attempts_label.pack(pady=6)

        self.guess_button = ttk.Button(master, text="🎯 Guess", command=self.check_guess)
        self.guess_button.pack(pady=6)

        self.result_label = ttk.Label(master, text="", font=("Segoe UI", 11, "bold"))
        self.result_label.pack(pady=10)

        self.play_again_button = ttk.Button(master, text="🔁 Play Again", command=self.reset_game)
        self.play_again_button.pack(pady=8)
        self.play_again_button.pack_forget()

        self.time_played_label = ttk.Label(master, text="", font=("Segoe UI", 10))
        self.time_played_label.pack(pady=8)

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            if 0 <= guess <= 10:
                self.attempts_left -= 1
                self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")

                if guess == self.number_to_guess:
                    self.result_label.config(text="✅ You guessed it right!")
                    self.end_game()
                elif self.attempts_left == 0:
                    self.result_label.config(text=f"❌ Oops No attempts left! The Correct Number was {self.number_to_guess}.")
                    self.end_game()
                else:
                    self.result_label.config(text="⚠️ Try again!")
                    self.entry.delete(0, tk.END)
            else:
                self.result_label.config(text="⚠️ Enter a number from 0 to 10.")
        except ValueError:
            self.result_label.config(text="⚠️ Enter a valid number.")

    def end_game(self):
        self.end_time = create_time()
        time_played = calculate_difference(self.start_time, self.end_time)
        self.time_played_label.config(text=f"⏱️ You played for {time_played:.2f} seconds.")
        self.play_again_button.pack()
        self.guess_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.DISABLED)

    def reset_game(self):
        self.number_to_guess = generate_random(10)
        self.start_time = create_time()
        self.attempts_left = 3
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.guess_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.NORMAL)
        self.play_again_button.pack_forget()
        self.time_played_label.config(text="")
        self.entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGameGUI(root)
    root.mainloop()
