# utils/game_helpers.py
import random
import tkinter as tk

def generate_maze_grid(size):
    """Generate a random maze grid with 0 as path and 1 as wall."""
    maze = []
    for i in range(size):
        row = []
        for j in range(size):
            # Set borders as walls, rest as random wall/path
            if i == 0 or j == 0 or i == size - 1 or j == size - 1:
                row.append(1)
            else:
                row.append(random.choice([0, 0, 1]))  # More 0s = more open paths
        maze.append(row)
    maze[1][1] = 0  # Start point
    maze[size - 2][size - 2] = 0  # End point
    return maze

def draw_maze(canvas, maze, cell_size):
    """Draw the maze on the canvas."""
    canvas.delete("all")  # Clear previous drawings
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            color = "black" if cell == 1 else "white"
            canvas.create_rectangle(
                j * cell_size, i * cell_size,
                (j + 1) * cell_size, (i + 1) * cell_size,
                fill=color
            )
    # Mark start and goal
    canvas.create_rectangle(1 * cell_size, 1 * cell_size, 2 * cell_size, 2 * cell_size, fill="blue")
    canvas.create_rectangle((len(maze) - 2) * cell_size, (len(maze) - 2) * cell_size,
                            (len(maze) - 1) * cell_size, (len(maze) - 1) * cell_size, fill="red")
