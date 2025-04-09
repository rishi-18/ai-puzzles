import tkinter as tk
from utils.game_helpers import generate_maze_grid, draw_maze, animate_path
from utils.ai_algorithms import a_star_search

CELL_SIZE = 40
GRID_SIZE = 10

class MazeEscapeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Escape")

        self.canvas = tk.Canvas(root, width=CELL_SIZE * GRID_SIZE, height=CELL_SIZE * GRID_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.maze_grid = []
        self.start = (0, 0)
        self.goal = (GRID_SIZE - 1, GRID_SIZE - 1)

        self.canvas.bind("<Button-1>", self.set_start)
        self.canvas.bind("<Button-3>", self.set_goal)

        tk.Button(root, text="Generate Maze", command=self.generate).grid(row=1, column=0, pady=10)
        tk.Button(root, text="Solve with AI", command=self.solve).grid(row=1, column=1, pady=10)
        tk.Label(root, text="Left-click: Start | Right-click: Goal", font=("Segoe UI", 9)).grid(row=1, column=2)

    def generate(self):
        while True:
            self.maze_grid = generate_maze_grid(GRID_SIZE)
            if a_star_search(self.maze_grid, self.start, self.goal):
                break
        draw_maze(self.canvas, self.maze_grid, CELL_SIZE, self.start, self.goal)

    def solve(self):
        if not self.maze_grid:
            return
        path = a_star_search(self.maze_grid, self.start, self.goal)
        if path:
            animate_path(self.canvas, path, CELL_SIZE)
        else:
            print("No path found.")

    def set_start(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if self.maze_grid and self.maze_grid[row][col] == 0:
            self.start = (row, col)
            draw_maze(self.canvas, self.maze_grid, CELL_SIZE, self.start, self.goal)

    def set_goal(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if self.maze_grid and self.maze_grid[row][col] == 0:
            self.goal = (row, col)
            draw_maze(self.canvas, self.maze_grid, CELL_SIZE, self.start, self.goal)

def run():
    window = tk.Toplevel()
    MazeEscapeGame(window)
    window.mainloop()
