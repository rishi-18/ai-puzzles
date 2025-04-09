# main.py
import tkinter as tk
from tkinter import messagebox

# Import game modules (make sure these exist in the /games folder)
from games import maze_escape, code_breaker, traffic_puzzle, n_queens

def launch_maze_escape():
    maze_escape.run()

def launch_code_breaker():
    code_breaker.run()

def launch_traffic_puzzle():
    traffic_puzzle.run()

def launch_n_queens():
    n_queens.run()

# Initialize main window
root = tk.Tk()
root.title("AI Puzzle Solver")
root.geometry("400x400")
root.resizable(False, False)

# Title label
tk.Label(root, text="AI Puzzle Solver", font=("Arial", 20, "bold")).pack(pady=20)

# Game selection buttons
tk.Button(root, text="Maze Escape", width=25, height=2, command=launch_maze_escape).pack(pady=10)
tk.Button(root, text="Code Breaker", width=25, height=2, command=launch_code_breaker).pack(pady=10)
tk.Button(root, text="Traffic Puzzle", width=25, height=2, command=launch_traffic_puzzle).pack(pady=10)
tk.Button(root, text="N-Queens Problem", width=25, height=2, command=launch_n_queens).pack(pady=10)

# Exit button
tk.Button(root, text="Exit", width=15, command=root.destroy).pack(pady=20)

root.mainloop()
