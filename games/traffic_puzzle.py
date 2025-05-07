import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from utils.game_helpers import TrafficPuzzleBoard
from utils.ai_algorithms import solve_traffic_puzzle

def get_initial_board(difficulty="easy"):
    if difficulty == "easy":
        return [
            ['A', 'A', '.', '.', '.', '.'],
            ['B', '.', '.', 'C', 'C', 'C'],
            ['B', 'R', 'R', '.', '.', '.'],
            ['D', 'D', '.', 'E', '.', '.'],
            ['.', '.', '.', 'E', 'F', 'F'],
            ['.', '.', '.', '.', '.', '.']
        ]
    elif difficulty == "medium":
        return [
            ['A', 'A', '.', '.', '.', '.'],
            ['.', '.', 'B', 'B', 'B', '.'],
            ['C', 'R', 'R', '.', 'D', '.'],
            ['C', '.', '.', '.', 'D', '.'],
            ['E', 'E', '.', 'F', 'F', 'F'],
            ['.', '.', '.', '.', '.', '.']
        ]
    elif difficulty == "hard":
        return [
            ['A', 'A', '.', 'B', 'B', 'B'],
            ['.', '.', '.', '.', '.', '.'],
            ['C', 'R', 'R', 'D', 'D', '.'],
            ['C', '.', '.', '.', '.', '.'],
            ['E', 'E', 'F', 'F', '.', '.'],
            ['.', '.', '.', '.', '.', '.']
        ]
    return []

class TrafficPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Puzzle Solver")

        # Controls frame
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=10)

        # Difficulty
        tk.Label(controls_frame, text="Difficulty:").grid(row=0, column=0, padx=5)
        self.difficulty_var = tk.StringVar(value="easy")
        difficulty_dropdown = ttk.Combobox(controls_frame, textvariable=self.difficulty_var, values=["easy", "medium", "hard"], width=8)
        difficulty_dropdown.grid(row=0, column=1)
        difficulty_dropdown.bind("<<ComboboxSelected>>", self.reload_board)

        # Algorithm
        tk.Label(controls_frame, text="Algorithm:").grid(row=0, column=2, padx=5)
        self.algorithm_var = tk.StringVar(value="A*")
        ttk.Combobox(controls_frame, textvariable=self.algorithm_var, values=["A*", "BFS", "DFS"], width=8).grid(row=0, column=3)

        # Animation toggle
        self.animate_var = tk.BooleanVar(value=True)
        tk.Checkbutton(controls_frame, text="Animate", variable=self.animate_var).grid(row=0, column=4, padx=10)

        # Puzzle board
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)

        self.board = None
        self.reload_board()

        # Solve button
        self.solve_button = tk.Button(self.root, text="Solve Puzzle", font=("Segoe UI", 12), command=self.solve_puzzle)
        self.solve_button.pack(pady=10)

    def reload_board(self, event=None):
        # Clear old widgets
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Load new board
        difficulty = self.difficulty_var.get()
        self.initial_board = get_initial_board(difficulty)
        self.board = TrafficPuzzleBoard(self.board_frame, self.initial_board)
        self.board.render_board()

    def solve_puzzle(self):
        algorithm = self.algorithm_var.get()
        animate = self.animate_var.get()
        board_state = self.board.get_board()

        solution = solve_traffic_puzzle(board_state, algorithm=algorithm)
        if solution:
            self.board.animate_solution(solution, animate=animate)
        else:
            messagebox.showinfo("No Solution", "No solution could be found for the current puzzle.")

def run():
    root = tk.Toplevel()
    app = TrafficPuzzleApp(root)
    root.mainloop()
