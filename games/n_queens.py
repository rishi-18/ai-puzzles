# games/n_queens.py

import tkinter as tk
from tkinter import messagebox
from utils.ai_algorithms import solve_n_queens

CELL_SIZE = 60

class NQueensGame:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Puzzle")

        tk.Label(root, text="Select N:", font=("Arial", 14)).grid(row=0, column=0)
        self.n_var = tk.IntVar(value=8)
        tk.Spinbox(root, from_=4, to=12, textvariable=self.n_var, width=5, font=("Arial", 14)).grid(row=0, column=1)

        tk.Button(root, text="Solve with AI", font=("Arial", 12), command=self.solve).grid(row=0, column=2, padx=5)
        tk.Button(root, text="Clear", font=("Arial", 12), command=self.clear_board).grid(row=0, column=3, padx=5)

        self.canvas = tk.Canvas(root, width=8 * CELL_SIZE, height=8 * CELL_SIZE, bg="#333")
        self.canvas.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        try:
            self.queen_img = tk.PhotoImage(file="assets/queen.png")
        except Exception:
            self.queen_img = None

        self.board_size = 8
        self.queen_ids = []

    def draw_board(self, n):
        self.canvas.config(width=n * CELL_SIZE, height=n * CELL_SIZE)
        self.canvas.delete("all")
        self.board_size = n
        for row in range(n):
            for col in range(n):
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(
                    col * CELL_SIZE, row * CELL_SIZE,
                    (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE,
                    fill=color, outline=""
                )

    def animate_solution(self, solution, i=0):
        if i >= len(solution):
            return
        row, col = i, solution[i]
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = row * CELL_SIZE + CELL_SIZE // 2
        if self.queen_img:
            img_id = self.canvas.create_text(x, y, text='♕', font=("Arial", CELL_SIZE // 2), fill="black")

        else:
            img_id = self.canvas.create_text(x, y, text='♕', font=("Arial", 28), fill="black")
        self.queen_ids.append(img_id)
        self.root.after(500, lambda: self.animate_solution(solution, i + 1))

    def solve(self):
        n = self.n_var.get()
        self.clear_board()
        self.draw_board(n)
        solution = solve_n_queens(n)
        if solution:
            self.animate_solution(solution)
        else:
            messagebox.showinfo("No Solution", f"No solution found for {n} queens.")

    def clear_board(self):
        self.canvas.delete("all")
        self.queen_ids.clear()

def run():
    root = tk.Toplevel()
    app = NQueensGame(root)
    app.draw_board(8)
    root.mainloop()
