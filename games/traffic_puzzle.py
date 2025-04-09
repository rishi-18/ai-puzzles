# import tkinter as tk
# from utils.game_helpers import TrafficPuzzleBoard
# from utils.ai_algorithms import solve_traffic_puzzle

# # Sample initial board configuration
# # 'R' represents the red (target) car that needs to be moved to the exit (right edge)
# # Each letter represents a different car
# # Empty cells are represented by '.'
# initial_board = [
#     ['A', 'A', '.', '.', '.', '.'],
#     ['B', '.', '.', 'C', 'C', 'C'],
#     ['B', 'R', 'R', '.', '.', '.'],
#     ['D', 'D', '.', 'E', '.', '.'],
#     ['.', '.', '.', 'E', 'F', 'F'],
#     ['.', '.', '.', '.', '.', '.']
# ]

# def run():
#     root = tk.Toplevel()
#     root.title("AI Traffic Puzzle Solver")

#     # Header label
#     header = tk.Label(root, text="Traffic Puzzle Solver", font=("Helvetica", 18, "bold"))
#     header.pack(pady=10)

#     # Create board object
#     board_frame = tk.Frame(root)
#     board_frame.pack()

#     board = TrafficPuzzleBoard(board_frame, initial_board)
#     board.render_board()

#     # Button to solve puzzle
#     def solve_puzzle():
#         solution = solve_traffic_puzzle(board.get_board())
#         if solution:
#             board.animate_solution(solution)
#         else:
#             tk.messagebox.showinfo("Traffic Puzzle", "No solution found.")

#     solve_button = tk.Button(root, text="Solve with AI", command=solve_puzzle)
#     solve_button.pack(pady=10)

#     root.mainloop()
