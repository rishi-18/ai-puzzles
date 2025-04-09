# utils/game_helpers.py

import random
import tkinter as tk

# ---------------------------
# MAZE UTILITIES
# ---------------------------

def generate_maze_grid(size):
    """
    Generates a random maze grid of given size.
    0 = path, 1 = wall.
    Ensures start and goal are always open.
    """
    grid = [[0 if random.random() > 0.3 else 1 for _ in range(size)] for _ in range(size)]
    grid[0][0] = 0
    grid[size - 1][size - 1] = 0
    return grid

def draw_maze(canvas, grid, cell_size):
    """
    Draws the maze grid on the canvas.
    Black = wall, White = open path.
    """
    canvas.delete("all")
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(
                j * cell_size, i * cell_size,
                (j + 1) * cell_size, (i + 1) * cell_size,
                fill=color,
                outline="gray"
            )


# ---------------------------
# N-QUEENS UTILITIES
# ---------------------------

def draw_chessboard(canvas, queens, size, cell_size):
    """
    Draws an N x N chessboard with queens.
    Queens is a list where index = row and value = column.
    """
    canvas.delete("all")

    for i in range(size):
        for j in range(size):
            color = "white" if (i + j) % 2 == 0 else "gray"
            canvas.create_rectangle(
                j * cell_size, i * cell_size,
                (j + 1) * cell_size, (i + 1) * cell_size,
                fill=color,
                outline="black"
            )

    for row, col in enumerate(queens):
        canvas.create_oval(
            col * cell_size + 10, row * cell_size + 10,
            (col + 1) * cell_size - 10, (row + 1) * cell_size - 10,
            fill="red"
        )


# ---------------------------
# CODE BREAKER UTILITIES
# ---------------------------

def generate_random_number(length):
    """
    Generates a unique-digit random number string of given length.
    Used for the secret code in Code Breaker.
    """
    digits = list("0123456789")
    random.shuffle(digits)
    return ''.join(digits[:length])


# ---------------------------
# GENERAL UTILS (Optional)
# ---------------------------

def show_popup(title, message):
    """
    Shows a simple popup dialog box.
    """
    popup = tk.Toplevel()
    popup.title(title)
    tk.Label(popup, text=message, padx=20, pady=10).pack()
    tk.Button(popup, text="OK", command=popup.destroy).pack(pady=(0, 10))
    popup.grab_set()  # Makes the popup modal
