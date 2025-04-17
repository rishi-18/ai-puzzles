import random
import random
import math

def generate_random_maze(grid_size):
    while True:
        maze = [[1 if random.random() < 0.35 else 0 for _ in range(grid_size)] for _ in range(grid_size)]
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
            if maze[i][j] == 1 and random.random() < 0.2:
                maze[i][j] = 0

def generate_circular_maze(grid_size):
    maze = [[1 for _ in range(grid_size)] for _ in range(grid_size)]
    cx, cy = grid_size // 2, grid_size // 2
    for i in range(grid_size):
        for j in range(grid_size):
            dist = math.sqrt((i - cx) ** 2 + (j - cy) ** 2)
            if dist < grid_size // 2 and random.random() > 0.3:
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
            if (sector % 2 == 0 and random.random() > 0.4) or (sector % 2 == 1 and random.random() > 0.8):
                maze[i][j] = 0
    maze[0][0] = 0
    maze[grid_size - 1][grid_size - 1] = 0
    return maze

def generate_maze_grid(size, maze_type="random"):
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
    from utils.ai_algorithms import a_star_search
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
                outline="gray"  # Add border for visibility
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

