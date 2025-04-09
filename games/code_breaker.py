# games/code_breaker.py

import tkinter as tk
from tkinter import messagebox
import random
from itertools import permutations

class CodeBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Code Breaker")
        self.secret_code = None
        self.possible_codes = [''.join(p) for p in permutations('0123456789', 4)]

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter your 4-digit secret code (unique digits):").pack(pady=5)
        self.entry = tk.Entry(self.root)
        self.entry.pack()

        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=10)

        self.output = tk.Text(self.root, height=15, width=50)
        self.output.pack()

    def start_game(self):
        code = self.entry.get()
        if not code.isdigit() or len(code) != 4 or len(set(code)) != 4:
            messagebox.showerror("Invalid", "Enter 4 unique digits!")
            return
        self.secret_code = code
        self.output.insert(tk.END, f"Secret code is set. AI will now guess...\n")
        self.run_ai()

    def feedback(self, guess):
        correct_place = sum(guess[i] == self.secret_code[i] for i in range(4))
        correct_digit = sum(min(guess.count(d), self.secret_code.count(d)) for d in set(guess)) - correct_place
        return correct_place, correct_digit

    def run_ai(self):
        attempts = 0
        while self.possible_codes:
            guess = random.choice(self.possible_codes)
            attempts += 1
            correct_place, correct_digit = self.feedback(guess)

            self.output.insert(tk.END, f"AI Guess {attempts}: {guess} → ✅: {correct_place}, ⚠️: {correct_digit}\n")
            self.output.see(tk.END)

            if guess == self.secret_code:
                self.output.insert(tk.END, f"\nAI cracked the code in {attempts} attempts!\n")
                break

            # Eliminate impossible guesses
            self.possible_codes = [
                code for code in self.possible_codes
                if self.feedback(code) == (correct_place, correct_digit)
            ]
