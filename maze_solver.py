import tkinter as tk
from tkinter import ttk, messagebox
import time
from maze_types import MazeFactory
from algorithms import AlgorithmFactory

class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Maze Solver")
        
        # Configuration
        self.maze_type = "2D"
        self.algorithm = "A*"
        self.maze_size = 15
        self.maze = None
        self.start = None
        self.goal = None
        self.solution_path = None
        
        # UI Setup
        self.setup_ui()
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25)
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Initial maze
        self.generate_maze()
    
    def setup_ui(self):
        # Control Frame
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="nsew")
        
        # Maze Type
        ttk.Label(control_frame, text="Maze Type:").grid(row=0, column=0, sticky="w")
        self.maze_type_var = tk.StringVar(value="2D")
        maze_types = ["2D", "3D", "Circular", "Hexagonal"]
        ttk.Combobox(control_frame, textvariable=self.maze_type_var, values=maze_types).grid(row=0, column=1, sticky="ew")
        
        # Algorithm
        ttk.Label(control_frame, text="Algorithm:").grid(row=1, column=0, sticky="w")
        self.algorithm_var = tk.StringVar(value="A*")
        algorithms = ["A*", "Dijkstra", "Bidirectional BFS", "DFS", "Greedy Best-First"]
        ttk.Combobox(control_frame, textvariable=self.algorithm_var, values=algorithms).grid(row=1, column=1, sticky="ew")
        
        # Size
        ttk.Label(control_frame, text="Maze Size:").grid(row=2, column=0, sticky="w")
        self.size_var = tk.IntVar(value=15)
        ttk.Spinbox(control_frame, from_=5, to=50, textvariable=self.size_var).grid(row=2, column=1, sticky="ew")
        
        # Buttons
        ttk.Button(control_frame, text="Generate Maze", command=self.generate_maze).grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        ttk.Button(control_frame, text="Solve", command=self.solve_maze).grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Maze Display
        self.maze_frame = ttk.Frame(self.root, padding="10")
        self.maze_frame.grid(row=1, column=0, sticky="nsew")
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var, relief="sunken").grid(row=2, column=0, sticky="ew")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
    
    def generate_maze(self):
        self.maze_type = self.maze_type_var.get()
        self.maze_size = self.size_var.get()
        
        try:
            factory = MazeFactory()
            self.maze = factory.create_maze(self.maze_type, self.maze_size)
            self.start = self.maze.get_start_position()
            self.goal = self.maze.get_goal_position()
            self.solution_path = None
            self.draw_maze()
            self.status_var.set(f"Generated {self.maze_type} maze (Size: {self.maze_size})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate maze: {str(e)}")
    
    def solve_maze(self):
        if not self.maze:
            messagebox.showwarning("Warning", "Please generate a maze first")
            return
            
        selected_algo = self.algorithm_var.get()
        
        try:
            # First solve with selected algorithm and show path
            self.solve_and_show(selected_algo)
            
            # Then compare all algorithms
            self.compare_and_show_results(selected_algo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to solve maze: {str(e)}")
    
    def solve_and_show(self, algorithm):
        start_time = time.time()
        factory = AlgorithmFactory()
        solver = factory.create_algorithm(algorithm)
        self.solution_path = solver.solve(self.maze, self.start, self.goal)
        elapsed = time.time() - start_time
        
        if self.solution_path:
            self.status_var.set(f"Solved with {algorithm} in {elapsed:.4f} sec")
            self.draw_maze()
            self.animate_solution()
        else:
            self.status_var.set(f"{algorithm} found no solution")
            self.draw_maze()
    
    def compare_and_show_results(self, selected_algo):
        results = []
        algorithms = ["A*", "Dijkstra", "Bidirectional BFS", "DFS", "Greedy Best-First"]
        
        for algo_name in algorithms:
            try:
                result = self.time_algorithm(algo_name)
                results.append(result)
            except Exception as e:
                results.append({
                    'algorithm': algo_name,
                    'time': 0,
                    'path_length': 0,
                    'solved': False,
                    'error': str(e)
                })

        self.show_results(results, selected_algo)
    
    def time_algorithm(self, algorithm):
        start_time = time.time()
        factory = AlgorithmFactory()
        solver = factory.create_algorithm(algorithm)
        path = solver.solve(self.maze, self.start, self.goal)
        elapsed = time.time() - start_time
        
        return {
            'algorithm': algorithm,
            'time': elapsed,
            'path_length': len(path) if path else 0,
            'solved': path is not None
        }
    
    def show_results(self, results, selected_algo):
        results_window = tk.Toplevel(self.root)
        results_window.title("Algorithm Comparison")
        results_window.geometry("500x350")
        
        frame = ttk.Frame(results_window)
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        tree = ttk.Treeview(frame, columns=('Algorithm', 'Time (s)', 'Path Length', 'Solved'), show='headings')
        tree.heading('Algorithm', text='Algorithm')
        tree.heading('Time (s)', text='Time (s)')
        tree.heading('Path Length', text='Path Length')
        tree.heading('Solved', text='Solved')
        
        for result in results:
            solved_text = "Yes" if result['solved'] else "No"
            time_text = f"{result['time']:.4f}"
            path_length = result['path_length'] if result['solved'] else "N/A"
            tags = ('selected',) if result['algorithm'] == selected_algo else ()
            
            tree.insert('', 'end', values=(
                result['algorithm'],
                time_text,
                path_length,
                solved_text
            ), tags=tags)
        
        tree.tag_configure('selected', background='lightblue')
        tree.pack(expand=True, fill='both')
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Find fastest successful algorithm
        successful = [r for r in results if r['solved']]
        if successful:
            fastest = min(successful, key=lambda x: x['time'])
            summary = f"Fastest: {fastest['algorithm']} ({fastest['time']:.4f}s)"
            ttk.Label(results_window, text=summary, font=('Helvetica', 10, 'bold')).pack(pady=5)
        
        # Add visualization button
        ttk.Button(
            results_window,
            text="Visualize Selected Algorithm",
            command=lambda: self.visualize_selected(tree)
        ).pack(pady=10)
    
    def visualize_selected(self, tree):
        selected = tree.focus()
        if selected:
            algo_name = tree.item(selected)['values'][0]
            self.solve_and_show(algo_name)
    
    def draw_maze(self):
        for widget in self.maze_frame.winfo_children():
            widget.destroy()
        canvas = self.maze.get_visualization(self.maze_frame)
        canvas.pack(expand=True, fill="both")
        self.maze_canvas = canvas
    
    def animate_solution(self):
        if self.solution_path and hasattr(self, 'maze_canvas'):
            self.maze.animate_path(self.maze_canvas, self.solution_path)

def run():
    root = tk.Tk()
    app = MazeSolverApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()