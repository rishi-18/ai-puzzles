import random
import time

def generate_maze_grid(size):
    grid = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
    grid[0][0] = 0
    grid[size - 1][size - 1] = 0
    return grid

def draw_maze(canvas, grid, cell_size, start=None, goal=None):
    canvas.delete("all")
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            color = "black" if val == 1 else "white"
            canvas.create_rectangle(
                j * cell_size, i * cell_size,
                (j + 1) * cell_size, (i + 1) * cell_size,
                fill=color
            )
    if start:
        i, j = start
        canvas.create_rectangle(
            j * cell_size, i * cell_size,
            (j + 1) * cell_size, (i + 1) * cell_size,
            fill="blue"
        )
    if goal:
        i, j = goal
        canvas.create_rectangle(
            j * cell_size, i * cell_size,
            (j + 1) * cell_size, (i + 1) * cell_size,
            fill="red"
        )

def animate_path(canvas, path, cell_size, delay=100):
    for i, (x, y) in enumerate(path):
        canvas.after(i * delay, lambda x=x, y=y: canvas.create_rectangle(
            y * cell_size, x * cell_size,
            (y + 1) * cell_size, (x + 1) * cell_size,
            fill="lightgreen"
        ))

