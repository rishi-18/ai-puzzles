import random
import math
import tkinter as tk
from abc import ABC, abstractmethod

class Maze(ABC):
    @abstractmethod
    def get_start_position(self):
        pass
    
    @abstractmethod
    def get_goal_position(self):
        pass
    
    @abstractmethod
    def get_visualization(self, parent):
        pass
    
    @abstractmethod
    def animate_path(self, canvas, path):
        pass
    
    @abstractmethod
    def get_neighbors(self, position):
        pass

class RectangularMaze2D(Maze):
    def __init__(self, size):
        self.size = size
        self.grid = self._generate_maze()
        self.start = (0, 0)
        self.goal = (size-1, size-1)
        
    def _generate_maze(self):
        # Generate a random 2D maze
        grid = [[0 if random.random() < 0.7 else 1 for _ in range(self.size)] 
                for _ in range(self.size)]
        
        # Ensure start and goal are open
        grid[0][0] = 0
        grid[self.size-1][self.size-1] = 0
        return grid
    
    def get_start_position(self):
        return self.start
    
    def get_goal_position(self):
        return self.goal
    
    def get_visualization(self, parent):
        cell_size = min(500 // self.size, 30)
        canvas = tk.Canvas(parent, width=self.size*cell_size, height=self.size*cell_size)
        
        for i in range(self.size):
            for j in range(self.size):
                color = "black" if self.grid[i][j] == 1 else "white"
                canvas.create_rectangle(
                    j*cell_size, i*cell_size,
                    (j+1)*cell_size, (i+1)*cell_size,
                    fill=color, outline="gray"
                )
        
        # Draw start and goal
        start_i, start_j = self.start
        goal_i, goal_j = self.goal
        canvas.create_rectangle(
            start_j*cell_size, start_i*cell_size,
            (start_j+1)*cell_size, (start_i+1)*cell_size,
            fill="blue", outline="gray"
        )
        canvas.create_rectangle(
            goal_j*cell_size, goal_i*cell_size,
            (goal_j+1)*cell_size, (goal_i+1)*cell_size,
            fill="red", outline="gray"
        )
        
        return canvas
    
    def animate_path(self, canvas, path):
        cell_size = min(500 // self.size, 30)
        for step, (i, j) in enumerate(path):
            canvas.after(50 * step, lambda i=i, j=j: canvas.create_rectangle(
                j*cell_size, i*cell_size,
                (j+1)*cell_size, (i+1)*cell_size,
                fill="lightgreen", outline="gray"
            ))
    
    def get_neighbors(self, position):
        i, j = position
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size and self.grid[ni][nj] == 0:
                neighbors.append((ni, nj))
        
        return neighbors

class RectangularMaze3D(RectangularMaze2D):
    def __init__(self, size):
        self.size = size
        self.depth = 3  # Fixed 3 layers for simplicity
        self.grid = self._generate_maze()
        self.start = (0, 0, 0)
        self.goal = (self.depth-1, size-1, size-1)
    
    def _generate_maze(self):
        # Generate a 3D maze with layers
        return [[[0 if random.random() < 0.7 else 1 for _ in range(self.size)] 
                for _ in range(self.size)] for _ in range(self.depth)]
    
    def get_start_position(self):
        return self.start
    
    def get_goal_position(self):
        return self.goal
    
    def get_visualization(self, parent):
        # For simplicity, we'll show one layer at a time
        self.current_layer = 0
        cell_size = min(500 // self.size, 30)
        
        frame = tk.Frame(parent)
        frame.pack(expand=True, fill="both")
        
        # Layer navigation
        nav_frame = tk.Frame(frame)
        nav_frame.pack()
        tk.Button(nav_frame, text="Previous", command=self.prev_layer).pack(side="left")
        tk.Button(nav_frame, text="Next", command=self.next_layer).pack(side="left")
        self.layer_label = tk.Label(nav_frame, text=f"Layer: {self.current_layer+1}/{self.depth}")
        self.layer_label.pack(side="left")
        
        # Canvas for maze
        canvas = tk.Canvas(frame, width=self.size*cell_size, height=self.size*cell_size)
        canvas.pack()
        
        self.maze_canvas = canvas
        self.draw_current_layer()
        
        return frame
    
    def draw_current_layer(self):
        cell_size = min(500 // self.size, 30)
        self.maze_canvas.delete("all")
        
        for i in range(self.size):
            for j in range(self.size):
                color = "black" if self.grid[self.current_layer][i][j] == 1 else "white"
                self.maze_canvas.create_rectangle(
                    j*cell_size, i*cell_size,
                    (j+1)*cell_size, (i+1)*cell_size,
                    fill=color, outline="gray"
                )
        
        # Draw start and goal if in current layer
        if self.start[0] == self.current_layer:
            _, i, j = self.start
            self.maze_canvas.create_rectangle(
                j*cell_size, i*cell_size,
                (j+1)*cell_size, (i+1)*cell_size,
                fill="blue", outline="gray"
            )
        
        if self.goal[0] == self.current_layer:
            _, i, j = self.goal
            self.maze_canvas.create_rectangle(
                j*cell_size, i*cell_size,
                (j+1)*cell_size, (i+1)*cell_size,
                fill="red", outline="gray"
            )
        
        self.layer_label.config(text=f"Layer: {self.current_layer+1}/{self.depth}")
    
    def prev_layer(self):
        if self.current_layer > 0:
            self.current_layer -= 1
            self.draw_current_layer()
    
    def next_layer(self):
        if self.current_layer < self.depth - 1:
            self.current_layer += 1
            self.draw_current_layer()
    
    def animate_path(self, canvas, path):
        # For 3D maze, we need to handle layer changes during animation
        cell_size = min(500 // self.size, 30)
        
        for step, (z, i, j) in enumerate(path):
            def draw_step(z=z, i=i, j=j):
                if z != self.current_layer:
                    self.current_layer = z
                    self.draw_current_layer()
                
                canvas.create_rectangle(
                    j*cell_size, i*cell_size,
                    (j+1)*cell_size, (i+1)*cell_size,
                    fill="lightgreen", outline="gray"
                )
            
            canvas.after(50 * step, draw_step)
    
    def get_neighbors(self, position):
        z, i, j = position
        neighbors = []
        directions = [(0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1), (-1, 0, 0), (1, 0, 0)]
        
        for dz, di, dj in directions:
            nz, ni, nj = z + dz, i + di, j + dj
            if (0 <= nz < self.depth and 0 <= ni < self.size and 0 <= nj < self.size and 
                self.grid[nz][ni][nj] == 0):
                neighbors.append((nz, ni, nj))
        
        return neighbors

class CircularMaze(Maze):
    def __init__(self, size):
        self.size = size
        self.rings = min(size, 10)  # Number of concentric circles
        self.sectors = min(size * 2, 36)  # Number of sectors per ring
        self.grid = self._generate_maze()
        self.start = (0, 0)  # Innermost ring, first sector
        self.goal = (self.rings-1, self.sectors//2)  # Outer ring, opposite side
    
    def _generate_maze(self):
        # Generate a circular maze with radial walls
        grid = [[0 if random.random() < 0.7 else 1 for _ in range(self.sectors)] 
                for _ in range(self.rings)]
        
        # Ensure start and goal are open
        grid[0][0] = 0
        grid[self.rings-1][self.sectors//2] = 0
        return grid
    
    def get_start_position(self):
        return self.start
    
    def get_goal_position(self):
        return self.goal
    
    def get_visualization(self, parent):
        canvas = tk.Canvas(parent, width=500, height=500)
        
        center_x, center_y = 250, 250
        max_radius = 200
        
        # Draw rings
        for ring in range(self.rings):
            radius = (ring + 1) * (max_radius / self.rings)
            canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline="black"
            )
        
        # Draw sectors and walls
        angle_step = 360 / self.sectors
        for sector in range(self.sectors):
            angle = math.radians(sector * angle_step)
            x = center_x + max_radius * math.sin(angle)
            y = center_y - max_radius * math.cos(angle)
            canvas.create_line(center_x, center_y, x, y, fill="black")
            
            # Draw walls (blocked paths)
            for ring in range(self.rings):
                if self.grid[ring][sector] == 1:
                    inner_r = ring * (max_radius / self.rings)
                    outer_r = (ring + 1) * (max_radius / self.rings)
                    start_angle = math.radians(sector * angle_step)
                    end_angle = math.radians((sector + 1) * angle_step)
                    
                    # Draw radial wall
                    x1 = center_x + inner_r * math.sin(start_angle)
                    y1 = center_y - inner_r * math.cos(start_angle)
                    x2 = center_x + outer_r * math.sin(start_angle)
                    y2 = center_y - outer_r * math.cos(start_angle)
                    canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
                    
                    # Draw tangential wall
                    if ring > 0 and self.grid[ring-1][sector] == 1:
                        x1 = center_x + inner_r * math.sin(start_angle)
                        y1 = center_y - inner_r * math.cos(start_angle)
                        x2 = center_x + inner_r * math.sin(end_angle)
                        y2 = center_y - inner_r * math.cos(end_angle)
                        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
        
        # Draw start and goal
        self.draw_position(canvas, center_x, center_y, max_radius, self.start, "blue")
        self.draw_position(canvas, center_x, center_y, max_radius, self.goal, "red")
        
        return canvas
    
    def draw_position(self, canvas, center_x, center_y, max_radius, pos, color):
        ring, sector = pos
        angle = math.radians(sector * (360 / self.sectors))
        r1 = ring * (max_radius / self.rings)
        r2 = (ring + 1) * (max_radius / self.rings)
        mid_r = (r1 + r2) / 2
        
        x = center_x + mid_r * math.sin(angle)
        y = center_y - mid_r * math.cos(angle)
        radius = max_radius / (self.rings * 3)
        
        canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color, outline="black"
        )
    
    def animate_path(self, canvas, path):
        center_x, center_y = 250, 250
        max_radius = 200
        
        for step, (ring, sector) in enumerate(path):
            def draw_step(ring=ring, sector=sector):
                self.draw_position(canvas, center_x, center_y, max_radius, (ring, sector), "lightgreen")
            
            canvas.after(50 * step, draw_step)
    
    def get_neighbors(self, position):
        ring, sector = position
        neighbors = []
        
        # Radial movement (in/out)
        if ring > 0 and self.grid[ring-1][sector] == 0:  # Inner ring
            neighbors.append((ring-1, sector))
        if ring < self.rings-1 and self.grid[ring+1][sector] == 0:  # Outer ring
            neighbors.append((ring+1, sector))
        
        # Tangential movement (clockwise/counter-clockwise)
        if self.grid[ring][(sector-1) % self.sectors] == 0:  # Counter-clockwise
            neighbors.append((ring, (sector-1) % self.sectors))
        if self.grid[ring][(sector+1) % self.sectors] == 0:  # Clockwise
            neighbors.append((ring, (sector+1) % self.sectors))
        
        return neighbors

class HexagonalMaze(Maze):
    def __init__(self, size):
        self.size = size
        self.grid = self._generate_maze()
        self.start = (0, 0)
        self.goal = (size-1, size-1)
    
    def _generate_maze(self):
        # Generate a hexagonal grid maze
        grid = [[0 if random.random() < 0.7 else 1 for _ in range(self.size)] 
                for _ in range(self.size)]
        
        # Ensure start and goal are open
        grid[0][0] = 0
        grid[self.size-1][self.size-1] = 0
        return grid
    
    def get_start_position(self):
        return self.start
    
    def get_goal_position(self):
        return self.goal
    
    def get_visualization(self, parent):
        cell_size = min(500 // self.size, 30)
        canvas = tk.Canvas(parent, width=self.size*cell_size*1.5, height=self.size*cell_size)
        
        for i in range(self.size):
            for j in range(self.size):
                x = j * cell_size * 1.5
                y = i * cell_size + (j % 2) * cell_size * 0.5
                
                # Draw hexagon
                points = [
                    x + cell_size * 0.5, y,
                    x + cell_size * 1.5, y,
                    x + cell_size * 2.0, y + cell_size * 0.5,
                    x + cell_size * 1.5, y + cell_size,
                    x + cell_size * 0.5, y + cell_size,
                    x, y + cell_size * 0.5
                ]
                
                color = "black" if self.grid[i][j] == 1 else "white"
                canvas.create_polygon(points, fill=color, outline="gray")
        
        # Draw start and goal
        self.draw_hex_position(canvas, cell_size, self.start, "blue")
        self.draw_hex_position(canvas, cell_size, self.goal, "red")
        
        return canvas
    
    def draw_hex_position(self, canvas, cell_size, pos, color):
        i, j = pos
        x = j * cell_size * 1.5
        y = i * cell_size + (j % 2) * cell_size * 0.5
        
        points = [
            x + cell_size * 0.5, y,
            x + cell_size * 1.5, y,
            x + cell_size * 2.0, y + cell_size * 0.5,
            x + cell_size * 1.5, y + cell_size,
            x + cell_size * 0.5, y + cell_size,
            x, y + cell_size * 0.5
        ]
        
        canvas.create_polygon(points, fill=color, outline="gray")
    
    def animate_path(self, canvas, path):
        cell_size = min(500 // self.size, 30)
        
        for step, (i, j) in enumerate(path):
            def draw_step(i=i, j=j):
                self.draw_hex_position(canvas, cell_size, (i, j), "lightgreen")
            
            canvas.after(50 * step, draw_step)
    
    def get_neighbors(self, position):
        i, j = position
        neighbors = []
        
        # Hexagonal neighbors depend on column parity
        offsets = [
            (-1, 0), (1, 0),  # Same column
            (0, -1), (0, 1),   # Left and right
        ]
        
        # Diagonal neighbors change based on column parity
        if j % 2 == 0:
            offsets.extend([(-1, -1), (-1, 1)])
        else:
            offsets.extend([(1, -1), (1, 1)])
        
        for di, dj in offsets:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size and self.grid[ni][nj] == 0:
                neighbors.append((ni, nj))
        
        return neighbors

class MazeFactory:
    def create_maze(self, maze_type, size):
        if maze_type == "2D":
            return RectangularMaze2D(size)
        elif maze_type == "3D":
            return RectangularMaze3D(size)
        elif maze_type == "Circular":
            return CircularMaze(size)
        elif maze_type == "Hexagonal":
            return HexagonalMaze(size)
        else:
            raise ValueError(f"Unknown maze type: {maze_type}")