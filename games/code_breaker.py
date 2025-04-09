import tkinter as tk
import random

class CodeBreakerManualFeedback:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Breaker - Manual Feedback Mode")
        self.code_length = 4
        self.max_attempts = 10
        self.guess_count = 0
        self.possible_digits = [str(i) for i in range(10)]
        self.past_guesses = []

        self.current_guess = self.generate_guess()

        self.setup_ui()
        self.display_guess()

    def setup_ui(self):
        self.title = tk.Label(self.root, text="Manual Feedback Mode", font=("Segoe UI", 14, "bold"))
        self.title.pack(pady=5)

        self.guess_display = tk.Label(self.root, text="", font=("Consolas", 14))
        self.guess_display.pack(pady=5)

        self.correct_pos_label = tk.Label(self.root, text="Correct Positions:")
        self.correct_pos_label.pack()
        self.correct_pos_entry = tk.Entry(self.root)
        self.correct_pos_entry.pack(pady=2)

        self.correct_digits_label = tk.Label(self.root, text="Correct Digits (Total):")
        self.correct_digits_label.pack()
        self.correct_digits_entry = tk.Entry(self.root)
        self.correct_digits_entry.pack(pady=2)

        self.submit_button = tk.Button(self.root, text="Submit Feedback", command=self.submit_feedback)
        self.submit_button.pack(pady=10)

        self.output_box = tk.Text(self.root, height=10, width=50, font=("Consolas", 11))
        self.output_box.pack(pady=10)
        self.output_box.configure(state="disabled")

    def display_guess(self):
        self.guess_display.config(text=f"AI Guess #{self.guess_count + 1}: {self.current_guess}")

    def generate_guess(self):
        while True:
            guess = ''.join(random.sample(self.possible_digits, self.code_length))
            if guess not in [g[0] for g in self.past_guesses]:
                return guess

    def output_message(self, message):
        self.output_box.configure(state="normal")
        self.output_box.insert(tk.END, message + "\n")
        self.output_box.configure(state="disabled")
        self.output_box.see(tk.END)

    def submit_feedback(self):
        try:
            correct_pos = int(self.correct_pos_entry.get())
            correct_digits = int(self.correct_digits_entry.get())
        except ValueError:
            self.output_message("❌ Please enter valid numbers.")
            return

        if correct_pos == self.code_length:
            self.output_message(f"✅ AI guessed the code '{self.current_guess}' correctly in {self.guess_count + 1} attempts!")
            self.submit_button.config(state="disabled")
            return

        self.past_guesses.append((self.current_guess, correct_pos, correct_digits))
        self.guess_count += 1

        if self.guess_count >= self.max_attempts:
            self.output_message("❌ AI failed to guess the code in 10 attempts.")
            self.submit_button.config(state="disabled")
            return

        self.correct_pos_entry.delete(0, tk.END)
        self.correct_digits_entry.delete(0, tk.END)

        self.current_guess = self.generate_guess()
        self.display_guess()

def run():
    root = tk.Toplevel()
    app = CodeBreakerManualFeedback(root)
    root.mainloop()
