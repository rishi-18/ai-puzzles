import random
import math

def generate_rectangular_maze(size):
    maze = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
    maze[0][0] = 0
    maze[size - 1][size - 1] = 0
    return maze

def generate_spiral_maze(size):
    maze = [[1] * size for _ in range(size)]
    value = 0
    for layer in range((size + 1) // 2):
        for i in range(layer, size - layer): maze[layer][i] = value
        for i in range(layer + 1, size - layer): maze[i][size - layer - 1] = value
        for i in range(size - layer - 2, layer - 1, -1): maze[size - layer - 1][i] = value
        for i in range(size - layer - 2, layer, -1): maze[i][layer] = value
    maze[0][0] = 0
    maze[size - 1][size - 1] = 0
    return maze

def generate_circular_maze(size):
    center = size // 2
    maze = [[1 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            dist = math.sqrt((i - center) ** 2 + (j - center) ** 2)
            if dist < center: maze[i][j] = 0
    maze[0][0] = 0
    maze[size - 1][size - 1] = 0
    return maze

def generate_radial_maze(grid_size):
    maze = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    cx, cy = grid_size // 2, grid_size // 2
    num_lines = 8
    for i in range(grid_size):
        for j in range(grid_size):
            angle = math.atan2(i - cx, j - cy)
            sector = int((angle + math.pi) / (2 * math.pi) * num_lines)
            if sector % 2 == 0:
                maze[i][j] = 1 if random.random() < 0.3 else 0
            else:
                maze[i][j] = 0
    maze[0][0] = 0
    maze[grid_size - 1][grid_size - 1] = 0
    return maze
