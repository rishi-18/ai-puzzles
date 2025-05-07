import random
import math
from utils.ai_algorithms import a_star_search

def generate_random_maze(grid_size):
    while True:
        maze = [[1 if random.random() < 0.5 else 0 for _ in range(grid_size)] for _ in range(grid_size)]
        maze[0][0], maze[grid_size - 1][grid_size - 1] = 0, 0
        if is_path_possible(maze):
            return maze

def generate_spiral_maze(grid_size):
    maze = [[1 for _ in range(grid_size)] for _ in range(grid_size)]
    x, y = 0, 0
    dx, dy = 0, 1
    steps = grid_size
    while steps > 0:
        for _ in range(steps):
            if 0 <= x < grid_size and 0 <= y < grid_size:
                maze[x][y] = 0
            x += dx
            y += dy
        x -= dx
        y -= dy
        dx, dy = dy, -dx
        x += dx
        y += dy
        steps -= 1
    add_spiral_branches(maze)
    maze[0][0] = 0
    maze[grid_size - 1][grid_size - 1] = 0
    return maze

def add_spiral_branches(maze):
    grid_size = len(maze)
    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            # Increase chance of branches to 0.5 for complexity
            if maze[i][j] == 1 and random.random() < 0.5:
                maze[i][j] = 0

def generate_circular_maze(grid_size):
    maze = [[1 for _ in range(grid_size)] for _ in range(grid_size)]
    cx, cy = grid_size // 2, grid_size // 2
    for i in range(grid_size):
        for j in range(grid_size):
            dist = math.sqrt((i - cx) ** 2 + (j - cy) ** 2)
            # Increase wall density by reducing openings
            if dist < grid_size // 2 and random.random() > 0.5:
                maze[i][j] = 0
    maze[0][0] = 0
    maze[grid_size - 1][grid_size - 1] = 0
    return maze

def generate_radial_maze(grid_size):
    maze = [[1 for _ in range(grid_size)] for _ in range(grid_size)]
    cx, cy = grid_size // 2, grid_size // 2
    for i in range(grid_size):
        for j in range(grid_size):
            angle = math.atan2(i - cx, j - cy)
            sector = int((angle + math.pi) / (2 * math.pi) * 16)
            # Increase walls by adjusting probabilities
            if (sector % 2 == 0 and random.random() > 0.6) or (sector % 2 == 1 and random.random() > 0.9):
                maze[i][j] = 0
    maze[0][0] = 0
    maze[grid_size - 1][grid_size - 1] = 0
    return maze

def generate_maze_grid(size, maze_type="rectangular"):
    if maze_type == "rectangular":
        return generate_random_maze(size)
    elif maze_type == "spiral":
        return generate_spiral_maze(size)
    elif maze_type == "circular":
        return generate_circular_maze(size)
    elif maze_type == "radial":
        return generate_radial_maze(size)
    else:
        raise ValueError(f"Unknown maze type: {maze_type}")

def is_path_possible(maze):
    return a_star_search(maze, (0, 0), (len(maze)-1, len(maze)-1)) is not None

def draw_maze(canvas, grid, cell_size, start=None, goal=None):
    canvas.delete("all")
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            color = "black" if val == 1 else "white"
            canvas.create_rectangle(
                j * cell_size, i * cell_size,
                (j + 1) * cell_size, (i + 1) * cell_size,
                fill=color,
                outline="gray"
            )
    if start:
        i, j = start
        canvas.create_rectangle(
            j * cell_size, i * cell_size,
            (j + 1) * cell_size, (i + 1) * cell_size,
            fill="blue",
            outline="gray"
        )
    if goal:
        i, j = goal
        canvas.create_rectangle(
            j * cell_size, i * cell_size,
            (j + 1) * cell_size, (i + 1) * cell_size,
            fill="red",
            outline="gray"
        )

def animate_path(canvas, path, cell_size, delay=100):
    for i, (x, y) in enumerate(path):
        canvas.after(i * delay, lambda x=x, y=y: canvas.create_rectangle(
            y * cell_size, x * cell_size,
            (y + 1) * cell_size, (x + 1) * cell_size,
            fill="lightgreen"
        ))

CELL_SIZE = 100

import tkinter as tk
import time

CELL_SIZE = 100
ANIMATION_DELAY = 0.3  # seconds between steps

class TrafficPuzzleBoard:
    def __init__(self, parent, board_data):
        self.parent = parent
        self.board_data = board_data
        self.rows = len(board_data)
        self.cols = len(board_data[0])
        self.cells = []

    def render_board(self):
        # Clear previous widgets
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.cells = []

        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                cell_value = self.board_data[r][c]
                label = tk.Label(self.parent, text=cell_value if cell_value != '.' else '',
                                 width=2, height=1, font=("Segoe UI", 20),
                                 borderwidth=2, relief="groove", bg=self.get_color(cell_value))
                label.grid(row=r, column=c, padx=1, pady=1)
                row.append(label)
            self.cells.append(row)

    def get_board(self):
        return [row[:] for row in self.board_data]

    def update_board(self, new_board):
        self.board_data = new_board
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.board_data[r][c]
                label = self.cells[r][c]
                label.config(text=value if value != '.' else '', bg=self.get_color(value))

    def animate_solution(self, solution_path, animate=True):
        if animate:
            for state in solution_path:
                self.update_board(state)
                self.parent.update()
                time.sleep(ANIMATION_DELAY)
        else:
            self.update_board(solution_path[-1])

    def get_color(self, value):
        # Assign a unique color per car, red for 'R', gray for empty
        if value == '.':
            return "lightgray"
        elif value == 'R':
            return "red"
        else:
            color_map = {
                'A': "#6EC1E4",
                'B': "#FFD966",
                'C': "#93C47D",
                'D': "#D9A7EB",
                'E': "#FFB6B9",
                'F': "#B4A7D6",
            }
            return color_map.get(value, "white")
