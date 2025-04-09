# games/maze_escape.py

import tkinter as tk
from utils.game_helpers import generate_maze_grid, draw_maze
from utils.ai_algorithms import a_star_search

CELL_SIZE = 40
GRID_SIZE = 10

class MazeEscapeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Escape")

        self.canvas = tk.Canvas(root, width=CELL_SIZE * GRID_SIZE, height=CELL_SIZE * GRID_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.maze_grid = []
        self.start = (0, 0)
        self.goal = (GRID_SIZE - 1, GRID_SIZE - 1)

        tk.Button(root, text="Generate Maze", command=self.generate).grid(row=1, column=0, pady=10)
        tk.Button(root, text="Solve with AI", command=self.solve).grid(row=1, column=1, pady=10)

    def generate(self):
        while True:
            self.maze_grid = generate_maze_grid(GRID_SIZE)
            path = a_star_search(self.maze_grid, self.start, self.goal)
            if path:
                break  # Maze is solvable
        draw_maze(self.canvas, self.maze_grid, CELL_SIZE)

    def solve(self):
        if not self.maze_grid:
            return
        path = a_star_search(self.maze_grid, self.start, self.goal)
        if path:
            for cell in path:
                x, y = cell
                self.canvas.create_rectangle(
                    y * CELL_SIZE, x * CELL_SIZE,
                    (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                    fill='lightgreen'
                )
        else:
            print("No path found.")
