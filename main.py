import tkinter as tk
from games import code_breaker, traffic_puzzle, n_queens
from maze_solver import run as run_maze_solver 

def start_code_breaker():
    code_breaker.run()

def start_traffic_puzzle():
    traffic_puzzle.run()

def start_n_queens():
    n_queens.run()

def start_advanced_maze_solver():
    run_maze_solver()

def on_enter(e):
    e.widget['background'] = current_theme['hover_bg']
    e.widget['foreground'] = current_theme['hover_fg']

def on_leave(e):
    e.widget['background'] = current_theme['button_bg']
    e.widget['foreground'] = current_theme['button_fg']

light_theme = {
    'bg': '#F5F5F5',
    'fg': '#333333',
    'sub_fg': '#555555',
    'button_bg': '#E6E6E6',
    'button_fg': 'black',
    'hover_bg': '#4B9CD3',
    'hover_fg': 'white'
}

dark_theme = {
    'bg': '#2E2E2E',
    'fg': '#F0F0F0',
    'sub_fg': '#AAAAAA',
    'button_bg': '#444',
    'button_fg': 'white',
    'hover_bg': '#6CA0DC',
    'hover_fg': 'white'
}

current_theme = light_theme

def toggle_theme():
    global current_theme
    current_theme = dark_theme if current_theme == light_theme else light_theme
    apply_theme()

def apply_theme():
    root.config(bg=current_theme['bg'])
    title_frame.config(bg=current_theme['bg'])
    btn_frame.config(bg=current_theme['bg'])
    title_label.config(bg=current_theme['bg'], fg=current_theme['fg'])
    subtitle_label.config(bg=current_theme['bg'], fg=current_theme['sub_fg'])
    theme_button.config(bg=current_theme['button_bg'], fg=current_theme['button_fg'])
    for btn in button_widgets:
        btn.config(bg=current_theme['button_bg'], fg=current_theme['button_fg'])

root = tk.Tk()
root.title("AI Puzzle Solver")
root.geometry("460x480")  
root.resizable(False, False)

title_frame = tk.Frame(root)
title_frame.pack(pady=30)  

title_label = tk.Label(
    title_frame,
    text="AI Puzzle Solver",
    font=("Georgia", 22, "bold")
)
title_label.pack()

subtitle_label = tk.Label(
    title_frame,
    text="Choose a puzzle to begin:",
    font=("Georgia", 14)
)
subtitle_label.pack(pady=(10, 20))  

btn_frame = tk.Frame(root)
btn_frame.pack()

button_style = {
    "font": ("Helvetica", 13),
    "width": 30,
    "relief": "raised",
    "bd": 2,
    "cursor": "hand2"
}

buttons = [
    ("🧩 Advanced Maze Solver", start_advanced_maze_solver),
    ("🔐 Code Breaker", start_code_breaker),
    ("🚗 Traffic Puzzle", start_traffic_puzzle),
    ("👑 N-Queens", start_n_queens)
]

button_widgets = []
for text, command in buttons:
    btn = tk.Button(btn_frame, text=text, command=command, **button_style)
    btn.pack(pady=8)  # Restored original padding
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    button_widgets.append(btn)

separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=10)

theme_button = tk.Button(
    root,
    text="🌗 Toggle Theme",
    font=("Helvetica", 11),
    command=toggle_theme
)
theme_button.pack(pady=15)  

apply_theme()
root.mainloop()