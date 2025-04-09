import heapq
from collections import deque
import copy

# a* algorithm for maze

def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    
    def heuristic(a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current_cost, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        neighbors = get_neighbors(current, rows, cols)
        for neighbor in neighbors:
            x, y = neighbor
            if grid[x][y] == 1:
                continue  # wall

            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, tentative_g, neighbor))

    return None  # No path found

def get_neighbors(pos, rows, cols):
    x, y = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append((nx, ny))
    
    return neighbors



# logic for traffic puzzle solver

def is_goal_state(board):
    for col in range(len(board[0]) - 1, -1, -1):
        if board[2][col] == 'R':
            return col == len(board[0]) - 1
    return False

def generate_moves(board):
    moves = []
    for r in range(6):
        for c in range(6):
            car = board[r][c]
            if car == '.' or (c > 0 and board[r][c-1] == car):
                continue

            # Horizontal movement
            if c < 5 and c + 1 < 6 and board[r][c + 1] == car:
                # Move left
                if c > 0 and board[r][c - 1] == '.':
                    new_board = copy.deepcopy(board)
                    i = 0
                    while c + i < 6 and new_board[r][c + i] == car:
                        i += 1
                    for j in range(i - 1, -1, -1):
                        new_board[r][c + j - 1] = car
                        new_board[r][c + j] = '.' if c + j < 6 else new_board[r][c + j]
                    moves.append(new_board)
                # Move right
                i = 0
                while c + i < 6 and board[r][c + i] == car:
                    i += 1
                if c + i < 6 and board[r][c + i] == '.':
                    new_board = copy.deepcopy(board)
                    for j in range(i - 1, -1, -1):
                        new_board[r][c + j + 1] = car
                        new_board[r][c + j] = '.' if j == 0 else new_board[r][c + j]
                    moves.append(new_board)

            # Vertical movement
            if r < 5 and r + 1 < 6 and board[r + 1][c] == car:
                # Move up
                if r > 0 and board[r - 1][c] == '.':
                    new_board = copy.deepcopy(board)
                    i = 0
                    while r + i < 6 and new_board[r + i][c] == car:
                        i += 1
                    for j in range(i - 1, -1, -1):
                        new_board[r + j - 1][c] = car
                        new_board[r + j][c] = '.' if r + j < 6 else new_board[r + j][c]
                    moves.append(new_board)
                # Move down
                i = 0
                while r + i < 6 and board[r + i][c] == car:
                    i += 1
                if r + i < 6 and board[r + i][c] == '.':
                    new_board = copy.deepcopy(board)
                    for j in range(i - 1, -1, -1):
                        new_board[r + j + 1][c] = car
                        new_board[r + j][c] = '.' if j == 0 else new_board[r + j][c]
                    moves.append(new_board)

    return moves

def traffic_puzzle_solver(initial_board):
    visited = set()
    queue = deque()
    queue.append((initial_board, []))


# solve n-queens problem

def solve_n_queens(n):
    def is_safe(queens, row, col):
        for r in range(row):
            c = queens[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def backtrack(row, queens):
        if row == n:
            return queens.copy()
        for col in range(n):
            if is_safe(queens, row, col):
                queens[row] = col
                result = backtrack(row + 1, queens)
                if result:
                    return result
        return None

    return backtrack(0, [-1] * n)

