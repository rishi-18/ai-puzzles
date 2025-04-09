# games/maze_escape.py
import tkinter as tk
from utils.game_helpers import generate_maze_grid, draw_maze
from utils.ai_algorithms import a_star_search

CELL_SIZE = 40  # Size of each square cell in pixels
GRID_SIZE = 10  # 10x10 maze

def run():
    root = tk.Toplevel()
    root.title("Maze Escape")

    canvas = tk.Canvas(root, width=CELL_SIZE * GRID_SIZE, height=CELL_SIZE * GRID_SIZE)
    canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Placeholder for maze grid and start/goal points
    maze_grid = []
    start = (0, 0)
    goal = (GRID_SIZE - 1, GRID_SIZE - 1)

    def generate():
        nonlocal maze_grid
        maze_grid = generate_maze_grid(GRID_SIZE)
        draw_maze(canvas, maze_grid, CELL_SIZE)

    def solve():
        if not maze_grid:
            return
        path = a_star_search(maze_grid, start, goal)
        if path:
            for cell in path:
                x, y = cell
                canvas.create_rectangle(
                    y * CELL_SIZE, x * CELL_SIZE,
                    (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                    fill='lightgreen'
                )
        else:
            print("No path found.")

    tk.Button(root, text="Generate Maze", command=generate).grid(row=1, column=0, pady=10)
    tk.Button(root, text="Solve with AI", command=solve).grid(row=1, column=1, pady=10)

    root.mainloop()
