import heapq
from collections import deque
import copy

# =========================
# A* Algorithm
# =========================

def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current, start)

        for neighbor in get_neighbors(current, rows, cols):
            x, y = neighbor
            if grid[x][y] == 1:
                continue  # Wall

            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                heapq.heappush(open_set, (tentative_g + heuristic(neighbor, goal), tentative_g, neighbor))

    return None


# =========================
# Dijkstra's Algorithm
# =========================

def dijkstra(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    dist = {start: 0}
    visited = set()
    pq = [(0, start)]
    came_from = {}

    while pq:
        current_dist, current = heapq.heappop(pq)
        if current == goal:
            return reconstruct_path(came_from, current, start)

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current, rows, cols):
            x, y = neighbor
            if grid[x][y] == 1:
                continue

            new_dist = current_dist + 1
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                came_from[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    return None


# =========================
# Bidirectional BFS
# =========================

def bidirectional_bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return None

    frontier_start = deque([start])
    frontier_goal = deque([goal])
    visited_start = {start: None}
    visited_goal = {goal: None}

    while frontier_start and frontier_goal:
        if path := expand_bfs_layer(frontier_start, visited_start, visited_goal, grid, rows, cols):
            return path
        if path := expand_bfs_layer(frontier_goal, visited_goal, visited_start, grid, rows, cols, reverse=True):
            return path

    return None


def expand_bfs_layer(frontier, visited, other_visited, grid, rows, cols, reverse=False):
    for _ in range(len(frontier)):
        current = frontier.popleft()
        for neighbor in get_neighbors(current, rows, cols):
            x, y = neighbor
            if grid[x][y] == 1 or neighbor in visited:
                continue
            visited[neighbor] = current
            if neighbor in other_visited:
                path_start = build_path(visited, neighbor)
                path_goal = build_path(other_visited, neighbor)
                if reverse:
                    path_start, path_goal = path_goal, path_start
                return path_start[::-1] + path_goal[1:]
            frontier.append(neighbor)
    return None


def build_path(came_from, end):
    path = []
    while end:
        path.append(end)
        end = came_from[end]
    return path[::-1]


# =========================
# Shared Utilities
# =========================

def get_neighbors(pos, rows, cols):
    x, y = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < rows and 0 <= y + dy < cols]

def reconstruct_path(came_from, current, start):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


# =========================
# Traffic Puzzle Solver
# =========================

def solve_traffic_puzzle(initial_board, algorithm="A*"):
    if algorithm == "BFS":
        return bfs(initial_board)
    elif algorithm == "DFS":
        return dfs(initial_board)
    else:
        return a_star(initial_board)

# ================= A* Search ================= #
def a_star(initial_board):
    def heuristic(state):
        # Heuristic: distance of red car (R) to exit
        for r in range(6):
            for c in range(6):
                if state[r][c] == 'R':
                    # Find the last R (assuming horizontal 2-long red car)
                    return 5 - c
        return float('inf')

    def serialize(board):
        return tuple(tuple(row) for row in board)

    visited = set()
    pq = []
    heapq.heappush(pq, (0 + heuristic(initial_board), 0, initial_board, [copy.deepcopy(initial_board)]))

    while pq:
        f, g, current, path = heapq.heappop(pq)
        if is_goal(current):
            return path
        key = serialize(current)
        if key in visited:
            continue
        visited.add(key)

        for next_state in generate_moves(current):
            next_path = path + [copy.deepcopy(next_state)]
            h = heuristic(next_state)
            heapq.heappush(pq, (g + 1 + h, g + 1, next_state, next_path))

    return None

# ================= BFS ================= #
def bfs(initial_board):
    visited = set()
    queue = deque()
    queue.append((initial_board, [copy.deepcopy(initial_board)]))
    visited.add(serialize(initial_board))

    while queue:
        current, path = queue.popleft()
        if is_goal(current):
            return path

        for next_state in generate_moves(current):
            key = serialize(next_state)
            if key not in visited:
                visited.add(key)
                queue.append((next_state, path + [copy.deepcopy(next_state)]))

    return None

# ================= DFS ================= #
def dfs(initial_board, depth_limit=50):
    visited = set()

    def dfs_recursive(state, path, depth):
        if is_goal(state):
            return path
        if depth > depth_limit:
            return None

        key = serialize(state)
        if key in visited:
            return None
        visited.add(key)

        for next_state in generate_moves(state):
            result = dfs_recursive(next_state, path + [copy.deepcopy(next_state)], depth + 1)
            if result:
                return result
        return None

    return dfs_recursive(initial_board, [copy.deepcopy(initial_board)], 0)

# ================= Helpers ================= #
def is_goal(board):
    # Goal: 'R' car reaches column 5
    for c in range(5, -1, -1):
        if board[2][c] == 'R':
            return c + 1 == 6  # right edge
    return False

def serialize(board):
    return tuple(tuple(row) for row in board)

def generate_moves(board):
    # VERY simplified move generator: only attempts moving 1 step left/right or up/down for any car
    moves = []
    rows, cols = 6, 6
    seen = set()

    for r in range(rows):
        for c in range(cols):
            car = board[r][c]
            if car == '.' or (r, c, car) in seen:
                continue
            seen.add((r, c, car))

            orientation = get_orientation(board, r, c)
            positions = get_car_positions(board, car)

            if orientation == 'horizontal':
                left_clear = min(col for _, col in positions) - 1
                right_clear = max(col for _, col in positions) + 1

                if 0 <= left_clear < cols and board[r][left_clear] == '.':
                    new_board = copy.deepcopy(board)
                    for _, col in reversed(positions):
                        new_board[r][col] = '.'
                    new_board[r][left_clear] = car
                    for _, col in positions[:-1]:
                        new_board[r][col + 1] = car
                    moves.append(new_board)

                if 0 <= right_clear < cols and board[r][right_clear] == '.':
                    new_board = copy.deepcopy(board)
                    for _, col in positions:
                        new_board[r][col] = '.'
                    new_board[r][right_clear] = car
                    for _, col in positions[1:]:
                        new_board[r][col - 1] = car
                    moves.append(new_board)

            elif orientation == 'vertical':
                top_clear = min(row for row, _ in positions) - 1
                bottom_clear = max(row for row, _ in positions) + 1

                if 0 <= top_clear < rows and board[top_clear][c] == '.':
                    new_board = copy.deepcopy(board)
                    for row, _ in reversed(positions):
                        new_board[row][c] = '.'
                    new_board[top_clear][c] = car
                    for row, _ in positions[:-1]:
                        new_board[row + 1][c] = car
                    moves.append(new_board)

                if 0 <= bottom_clear < rows and board[bottom_clear][c] == '.':
                    new_board = copy.deepcopy(board)
                    for row, _ in positions:
                        new_board[row][c] = '.'
                    new_board[bottom_clear][c] = car
                    for row, _ in positions[1:]:
                        new_board[row - 1][c] = car
                    moves.append(new_board)

    return moves

def get_car_positions(board, car):
    return [(r, c) for r in range(6) for c in range(6) if board[r][c] == car]

def get_orientation(board, r, c):
    car = board[r][c]
    if c + 1 < 6 and board[r][c + 1] == car:
        return 'horizontal'
    if r + 1 < 6 and board[r + 1][c] == car:
        return 'vertical'
    return 'horizontal'  # Default fallback


# n queens problem solver

def solve_n_queens(n):
    solutions = []

    def is_safe(queens, row, col):
        for r in range(row):
            c = queens[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def solve(queens, row):
        if row == n:
            solutions.append(queens[:])
            return
        for col in range(n):
            if is_safe(queens, row, col):
                queens[row] = col
                solve(queens, row + 1)

    solve([-1] * n, 0)
    return solutions[0] if solutions else None  
