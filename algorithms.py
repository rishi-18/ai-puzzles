import heapq
from collections import deque
from abc import ABC, abstractmethod

class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze, start, goal):
        pass

class AStarSolver(MazeSolver):
    def heuristic(self, a, b):
        if len(a) == 2:  # 2D
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        else:  # 3D
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
    
    def solve(self, maze, start, goal):
        open_set = []
        heapq.heappush(open_set, (self.heuristic(start, goal), 0, start))
        came_from = {}
        g_score = {start: 0}
        
        while open_set:
            _, cost, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            for neighbor in maze.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
        
        return []

class DijkstraSolver(MazeSolver):
    def solve(self, maze, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        dist = {start: 0}
        
        while open_set:
            cost, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            for neighbor in maze.get_neighbors(current):
                new_cost = dist[current] + 1
                if neighbor not in dist or new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (new_cost, neighbor))
        
        return []

class BidirectionalBFSSolver(MazeSolver):
    def solve(self, maze, start, goal):
        if start == goal:
            return [start]
        
        queue_start = deque([start])
        queue_goal = deque([goal])
        visited_start = {start: None}
        visited_goal = {goal: None}
        meet_node = None
        
        while queue_start and queue_goal:
            current_start = queue_start.popleft()
            for neighbor in maze.get_neighbors(current_start):
                if neighbor not in visited_start:
                    visited_start[neighbor] = current_start
                    queue_start.append(neighbor)
                    if neighbor in visited_goal:
                        meet_node = neighbor
                        break
            if meet_node:
                break
            
            current_goal = queue_goal.popleft()
            for neighbor in maze.get_neighbors(current_goal):
                if neighbor not in visited_goal:
                    visited_goal[neighbor] = current_goal
                    queue_goal.append(neighbor)
                    if neighbor in visited_start:
                        meet_node = neighbor
                        break
            if meet_node:
                break
        
        if not meet_node:
            return []
        
        path_start = []
        node = meet_node
        while node != start:
            path_start.append(node)
            node = visited_start[node]
        path_start.append(start)
        path_start.reverse()
        
        path_goal = []
        node = meet_node
        while node != goal:
            node = visited_goal[node]
            path_goal.append(node)
        
        return path_start + path_goal

class DFSSolver(MazeSolver):
    def solve(self, maze, start, goal):
        stack = [(start, [start])]
        visited = set()
        
        while stack:
            current, path = stack.pop()
            if current == goal:
                return path
            
            if current not in visited:
                visited.add(current)
                for neighbor in reversed(maze.get_neighbors(current)):
                    stack.append((neighbor, path + [neighbor]))
        
        return []

class GreedyBestFirstSolver(MazeSolver):
    def heuristic(self, a, b):
        if len(a) == 2:  # 2D
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        else:  # 3D
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
    
    def solve(self, maze, start, goal):
        open_set = []
        heapq.heappush(open_set, (self.heuristic(start, goal), start))
        came_from = {}
        came_from[start] = None
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            for neighbor in maze.get_neighbors(current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (self.heuristic(neighbor, goal), neighbor))
        
        return []

class AlgorithmFactory:
    def create_algorithm(self, algorithm_name):
        if algorithm_name == "A*":
            return AStarSolver()
        elif algorithm_name == "Dijkstra":
            return DijkstraSolver()
        elif algorithm_name == "Bidirectional BFS":
            return BidirectionalBFSSolver()
        elif algorithm_name == "DFS":
            return DFSSolver()
        elif algorithm_name == "Greedy Best-First":
            return GreedyBestFirstSolver()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")