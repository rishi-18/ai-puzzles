import heapq
import random

# ----------------------------
# A* Search Algorithm (Maze Escape & Traffic Puzzle)
# ----------------------------

def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    priority = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

    return None


# ----------------------------
# Backtracking (N-Queens)
# ----------------------------

def solve_n_queens(n):
    solutions = []

    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

    def backtrack(row, board):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1, board)

    board = [-1] * n
    backtrack(0, board)
    return solutions


# ----------------------------
# Code Breaker / Mastermind CSP (Randomized strategy with logic)
# ----------------------------

def generate_code(length=4):
    return [random.randint(0, 9) for _ in range(length)]

def evaluate_guess(secret, guess):
    correct = sum(s == g for s, g in zip(secret, guess))
    misplaced = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - correct
    return correct, misplaced

def basic_code_solver(secret, max_attempts=10):
    attempts = []
    possible_digits = list(range(10))

    for _ in range(max_attempts):
        guess = [random.choice(possible_digits) for _ in range(len(secret))]
        correct, misplaced = evaluate_guess(secret, guess)
        attempts.append((guess, correct, misplaced))
        if correct == len(secret):
            return guess, attempts
    return None, attempts


# ----------------------------
# Traffic Puzzle (Simple Heuristic for Grid Movement)
# ----------------------------

def traffic_solver(grid, target_car_pos, exit_pos):
    # Very simplified version using A* on car movement grid
    return a_star_search(grid, target_car_pos, exit_pos)
