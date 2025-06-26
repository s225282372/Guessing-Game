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

def save_high_score(time_played):
    with open("highscore.txt", "a") as f:
        f.write(f"{time_played:.2f}\n")

def get_best_time():
    try:
        with open("highscore.txt") as f:
            scores = [float(x.strip()) for x in f.readlines()]
            return min(scores) if scores else None
    except FileNotFoundError:
        return None

class GuessingGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("🎮 Guessing Game")
        master.geometry("420x440")
        master.configure(bg="#1e1e2f")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.set_dark_theme()

        # Theme Toggle
        self.theme = tk.StringVar(value="dark")
        ttk.Checkbutton(master, text="🌗 Light Theme", variable=self.theme, onvalue="light", offvalue="dark", command=self.toggle_theme).pack(pady=4)

        # Difficulty Selection Frame
        self.difficulty = tk.StringVar(value="Easy")
        self.difficulty_buttons = []

        difficulty_frame = ttk.LabelFrame(master, text="🎯 Difficulty Level", padding=(10, 5))
        difficulty_frame.pack(pady=10)

        for text, val in [("Easy (0–10)", "Easy"), ("Medium (0–25)", "Medium"), ("Hard (0–50)", "Hard")]:
            btn = ttk.Radiobutton(difficulty_frame, text=text, variable=self.difficulty, value=val)
            btn.pack(side=tk.LEFT, padx=10)
            self.difficulty_buttons.append(btn)

        # Game variables
        self.number_to_guess = None
        self.attempts_left = 0
        self.start_time = 0
        self.key_binding_id = None

        # Main UI
        self.label = ttk.Label(master, text="Enter your guess:")
        self.label.pack(pady=12)

        self.entry = ttk.Entry(master, width=18)
        self.entry.pack(pady=6)

        self.attempts_label = ttk.Label(master, text="")
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

        self.reset_game()

    def get_max_number_and_attempts(self):
        if self.difficulty.get() == "Easy":
            return 10, 3
        elif self.difficulty.get() == "Medium":
            return 25, 4
        else:
            return 50, 5

    def check_guess(self):
        if self.attempts_left <= 0:
            return

        try:
            guess = int(self.entry.get())
            max_val, _ = self.get_max_number_and_attempts()
            if 0 <= guess <= max_val:
                self.attempts_left -= 1
                self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")

                if guess == self.number_to_guess:
                    self.result_label.config(text="✅ You guessed it right!")
                    self.end_game()
                elif self.attempts_left == 0:
                    self.result_label.config(text=f"❌ No attempts left! It was {self.number_to_guess}.")
                    self.end_game()
                else:
                    self.result_label.config(text="⚠️ Try again!")
                    self.entry.delete(0, tk.END)
            else:
                self.result_label.config(text=f"⚠️ Enter a number between 0 and {max_val}.")
        except ValueError:
            self.result_label.config(text="⚠️ Enter a valid number.")

    def end_game(self):
        end_time = create_time()
        time_played = calculate_difference(self.start_time, end_time)
        best = get_best_time()

        if best:
            self.time_played_label.config(text=f"⏱️ You played for {time_played:.2f}s. Best: {best:.2f}s")
        else:
            self.time_played_label.config(text=f"⏱️ You played for {time_played:.2f}s")

        save_high_score(time_played)

        self.guess_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.DISABLED)
        self.play_again_button.pack()
        self.unbind_enter()
        self.enable_difficulty_buttons()

    def reset_game(self):
        max_val, attempts = self.get_max_number_and_attempts()
        self.number_to_guess = generate_random(max_val)
        self.attempts_left = attempts
        self.start_time = create_time()

        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.config(state=tk.NORMAL)
        self.entry.focus()
        self.guess_button.config(state=tk.NORMAL)
        self.play_again_button.pack_forget()
        self.time_played_label.config(text="")

        self.bind_enter()
        self.disable_difficulty_buttons()

    def bind_enter(self):
        self.key_binding_id = self.master.bind('<Return>', lambda event: self.check_guess())

    def unbind_enter(self):
        if self.key_binding_id:
            self.master.unbind('<Return>')
            self.key_binding_id = None

    def toggle_theme(self):
        if self.theme.get() == "light":
            self.set_light_theme()
        else:
            self.set_dark_theme()

    def set_dark_theme(self):
        self.master.configure(bg="#1e1e2f")
        self.style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 12))
        self.style.configure("TLabelframe", background="#1e1e2f", foreground="white")
        self.style.configure("TButton", font=("Segoe UI", 11), padding=8)
        self.style.configure("TEntry", padding=6, font=("Segoe UI", 11))

    def set_light_theme(self):
        self.master.configure(bg="white")
        self.style.configure("TLabel", background="white", foreground="black", font=("Segoe UI", 12))
        self.style.configure("TLabelframe", background="white", foreground="black")
        self.style.configure("TButton", font=("Segoe UI", 11), padding=8)
        self.style.configure("TEntry", padding=6, font=("Segoe UI", 11))

    def disable_difficulty_buttons(self):
        for btn in self.difficulty_buttons:
            btn.config(state=tk.DISABLED)

    def enable_difficulty_buttons(self):
        for btn in self.difficulty_buttons:
            btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGameGUI(root)
    root.mainloop()
