import tkinter as tk
from tkinter import ttk
import random
import time
import json


def create_time():
    return time.time()


def calculate_difference(start, end):
    return end - start


def generate_random(max_num):
    return random.randint(0, max_num)


def save_high_score(time_played, difficulty):
    data = load_scores()
    if difficulty not in data:
        data[difficulty] = []
    data[difficulty].append(time_played)
    with open("highscores.json", "w") as f:
        json.dump(data, f)


def load_scores():
    try:
        with open("highscores.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_best_time(difficulty):
    data = load_scores()
    scores = data.get(difficulty, [])
    return min(scores) if scores else None


def get_max_number_and_attempts(difficulty):
    settings = {
        "Easy": (10, 3),
        "Medium": (25, 4),
        "Hard": (50, 5),
        "Expert": (100, 6)
    }
    return settings.get(difficulty, (10, 3))


class GuessingGameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Guessing Game")
        master.geometry("450x550")
        master.configure(bg="#1e1e2f")


        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.set_dark_theme()

        self.games_played = 0
        self.games_won = 0

        self.theme = tk.StringVar(value="dark")
        theme_frame = ttk.Frame(master)
        theme_frame.pack(pady=5)
        ttk.Checkbutton(theme_frame, text="Light Theme", variable=self.theme,
                        onvalue="light", offvalue="dark", command=self.toggle_theme).pack()

        self.stats_frame = ttk.LabelFrame(master, text="Statistics", padding=(10, 5))
        self.stats_frame.pack(pady=5, padx=20, fill="x")
        self.stats_label = ttk.Label(self.stats_frame, text="Games Played: 0 | Won: 0 | Win Rate: 0%")
        self.stats_label.pack()

        self.difficulty = tk.StringVar(value="Easy")
        self.difficulty_buttons = []

        difficulty_frame = ttk.LabelFrame(master, text="Select Difficulty")
        difficulty_frame.pack(pady=10, padx=20, fill="x")

        difficulties = [
            ("Easy (0–10)", "Easy"),
            ("Medium (0–25)", "Medium"),
            ("Hard (0–50)", "Hard"),
            ("Expert (0–100)", "Expert")
        ]

        for text, val in difficulties:
            btn = ttk.Radiobutton(difficulty_frame, text=text, variable=self.difficulty, value=val)
            btn.pack(anchor="w", padx=5, pady=2)
            self.difficulty_buttons.append(btn)

        self.number_to_guess = None
        self.attempts_left = 0
        self.max_attempts = 0
        self.start_time = 0
        self.key_binding_id = None
        self.guess_history = []
        self.game_started = False

        game_frame = ttk.LabelFrame(master, text="Game", padding=(15, 10))
        game_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.label = ttk.Label(game_frame, text="Enter your guess:")
        self.label.pack(pady=(0, 8))

        self.entry = ttk.Entry(game_frame, width=20, font=("Segoe UI", 12))
        self.entry.pack(pady=6)

        self.attempts_label = ttk.Label(game_frame, text="")
        self.attempts_label.pack(pady=6)

        self.guess_button = ttk.Button(game_frame, text="🎯 Guess", command=self.check_guess)
        self.guess_button.pack(pady=8)

        self.result_label = ttk.Label(game_frame, text="", font=("Segoe UI", 11, "bold"))
        self.result_label.pack(pady=10)

        self.hint_label = ttk.Label(game_frame, text="", font=("Segoe UI", 10))
        self.hint_label.pack(pady=5)

        self.history_label = ttk.Label(game_frame, text="", font=("Segoe UI", 9))
        self.history_label.pack(pady=5)

        button_frame = ttk.Frame(game_frame)
        button_frame.pack(pady=10)

        self.play_again_button = ttk.Button(button_frame, text="🔁Play Again", command=self.reset_game)
        self.play_again_button.pack(side="left", padx=5)

        self.hint_button = ttk.Button(button_frame, text="💡Hint", command=self.show_hint)
        self.hint_button.pack(side="left", padx=5)

        self.scores_button = ttk.Button(button_frame, text="📋Scores", command=self.show_high_scores)
        self.scores_button.pack(side="right", padx=5)

        self.time_played_label = ttk.Label(game_frame, text="", font=("Segoe UI", 10))
        self.time_played_label.pack(pady=8)

        self.reset_game()

    def check_guess(self):
        if not self.game_started:
            self.start_game()

        if self.attempts_left <= 0:
            return

        try:
            guess = int(self.entry.get())
            max_val, _ = get_max_number_and_attempts(self.difficulty.get())
            if 0 <= guess <= max_val:
                self.attempts_left -= 1
                self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")

                if guess == self.number_to_guess:
                    self.result_label.config(text="🎉 Correct! You're a genius! 🎯 You guessed it right!")
                    self.games_won += 1
                    self.end_game()
                elif self.attempts_left == 0:
                    self.result_label.config(text=f"🫡Oops No attempts left! Correct Number was {self.number_to_guess}.")
                    self.end_game()
                else:
                    self.result_label.config(text="⚠️ Try again!")
                    self.entry.delete(0, tk.END)
            else:
                self.result_label.config(text=f"⚠️ Enter a number between 0 and {max_val}.")
        except ValueError:
            self.result_label.config(text="⚠️ Enter a valid number.")

    def start_game(self):
        max_val, attempts = get_max_number_and_attempts(self.difficulty.get())
        self.number_to_guess = generate_random(max_val)
        self.attempts_left = attempts
        self.start_time = create_time()
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.disable_difficulty_buttons()
        self.game_started = True

    def end_game(self):
        self.games_played += 1
        end_time = create_time()
        time_played = calculate_difference(self.start_time, end_time)
        difficulty = self.difficulty.get()
        best = get_best_time(difficulty)

        if best:
            self.time_played_label.config(text=f"⏱️ You played for {time_played:.2f}s. Best: {best:.2f}s")
        else:
            self.time_played_label.config(text=f"⏱️ You played for {time_played:.2f}s")

        save_high_score(time_played, difficulty)
        self.guess_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.DISABLED)
        self.play_again_button.pack(side="left", padx=5)
        self.unbind_enter()
        self.enable_difficulty_buttons()
        self.update_statistics()

    def reset_game(self):
        self.number_to_guess = None
        self.attempts_left = 0
        self.max_attempts = 0
        self.start_time = 0
        self.guess_history = []
        self.game_started = False

        self.attempts_label.config(text="")
        self.result_label.config(text="")
        self.hint_label.config(text="")
        self.history_label.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.config(state=tk.NORMAL)
        self.entry.focus()
        self.guess_button.config(state=tk.NORMAL)
        self.time_played_label.config(text="")

        self.bind_enter()

    def update_statistics(self):
        win_rate = (self.games_won / self.games_played * 100) if self.games_played > 0 else 0
        stats_text = f"Games Played: {self.games_played} | Won: {self.games_won} | Win Rate: {win_rate:.1f}%"
        self.stats_label.config(text=stats_text)

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
        self.style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 10))
        self.style.configure("TLabelframe", background="#1e1e2f", foreground="white")
        self.style.configure("TLabelframe.Label", background="#1e1e2f", foreground="white")
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TEntry", padding=6, font=("Segoe UI", 11))
        self.style.configure("TFrame", background="#1e1e2f")

    def set_light_theme(self):
        self.master.configure(bg="white")
        self.style.configure("TLabel", background="white", foreground="black", font=("Segoe UI", 10))
        self.style.configure("TLabelframe", background="white", foreground="black")
        self.style.configure("TLabelframe.Label", background="white", foreground="black")
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TEntry", padding=6, font=("Segoe UI", 11))
        self.style.configure("TFrame", background="white")

    def disable_difficulty_buttons(self):
        for btn in self.difficulty_buttons:
            btn.config(state=tk.DISABLED)

    def enable_difficulty_buttons(self):
        for btn in self.difficulty_buttons:
            btn.config(state=tk.NORMAL)

    def show_hint(self):
        if self.number_to_guess is None:
            return

        hint = "even" if self.number_to_guess % 2 == 0 else "odd"
        self.hint_label.config(text=f"Hint: The number is {hint}.")
        self.hint_button.config(state=tk.DISABLED)

    def show_high_scores(self):
        scores_window = tk.Toplevel(self.master)
        scores_window.title("High Scores")
        scores_window.geometry("300x400")
        scores_window.configure(bg=self.master.cget("bg"))


        if self.theme.get() == "dark":
            scores_window.configure(bg="#1e1e2f")
        else:
            scores_window.configure(bg="white")

        data = load_scores()

        ttk.Label(scores_window, text="High Scores", font=("Segoe UI", 14, "bold")).pack(pady=10)

        canvas = tk.Canvas(scores_window, bg=scores_window.cget("bg"), highlightthickness=0)
        scrollbar = ttk.Scrollbar(scores_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        if not data:
            ttk.Label(scrollable_frame, text="No scores yet!", font=("Segoe UI", 12)).pack(pady=20)
        else:
            for difficulty in ["Easy", "Medium", "Hard", "Expert"]:
                if difficulty in data and data[difficulty]:
                    scores = sorted(data[difficulty])[:10]
                    ttk.Label(scrollable_frame, text=f"{difficulty}:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
                    for i, score in enumerate(scores, 1):
                        score_text = f"{i:2d}. {score:.2f}s"
                        ttk.Label(scrollable_frame, text=score_text, font=("Segoe UI", 10)).pack(anchor="w", padx=20)

        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

        ttk.Button(scores_window, text="Close", command=scores_window.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGameGUI(root)
    root.mainloop()
