import tkinter as tk
from tkinter import messagebox
import time
from tkinter import ttk
import random
# Constants
EMPTY = 0
BLUE = 1
RED = 2
BOARD_ROWS = 6
BOARD_COLS = 7
Algo=0
Diffcality=0


# Create the main window
root = tk.Tk()
root.title("Connect Four")

# Initialize the game board
board = [[EMPTY] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Create a list to hold the buttons
buttons = []

# Create a variable to keep track of the current player
current_player = BLUE

class GUI:
 def __init__(self):
        self.window = tk.Tk()
        self.window.configure(bg='#486077')
        self.current_page = 1
        self.board = [[None] * 7 for _ in range(6)]
        self.current_player = "red"
        self.create_first_page()
        style = ttk.Style()
        style.configure("red.TButton", foreground="red")
        style.configure("blue.TButton", foreground="blue")
        
 def create_first_page(self):
        self.clear_window()

        style = ttk.Style()
        style.configure('Custom.TButton', background='gray', foreground='black',
                        font=('Arial', 12, 'bold'), relief=tk.RAISED)
        style.map('Custom.TButton',
                  background=[('active', '#222222')])

        frame = ttk.Frame(self.window, style='Custom.TFrame', padding=20)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        button1 = ttk.Button(frame, text="MiniMax", command=lambda: self.go_to_second_page(1), style='Custom.TButton')
        button1.pack(pady=10)

        button2 = ttk.Button(frame, text="MiniMax With Alpha-Beta", command=lambda: self.go_to_second_page(2), style='Custom.TButton')
        button2.pack(pady=10)

 def create_second_page(self):
        self.clear_window()

        style = ttk.Style()
        style.configure('Custom.TButton', background='gray', foreground='black',
                        font=('Arial', 12, 'bold'), relief=tk.RAISED)
        style.map('Custom.TButton',
                  background=[('active', '#222222')])

        frame = ttk.Frame(self.window, style='Custom.TFrame', padding=20)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        button1 = ttk.Button(frame, text="Low", command=lambda: self.go_to_final_page(1), style='Custom.TButton')
        button1.pack(pady=10)

        button2 = ttk.Button(frame, text="Medium", command=lambda: self.go_to_final_page(2), style='Custom.TButton')
        button2.pack(pady=10)

        button3 = ttk.Button(frame, text="High", command=lambda: self.go_to_final_page(3), style='Custom.TButton')
        button3.pack(pady=10)

    

   

 def go_to_second_page(self, button_id):
        print("Button {} on the first page is selected.".format(button_id))
        global Algo
        Algo=button_id
        self.current_page = 2
        self.create_second_page()

 def go_to_final_page(self, button_id):
        print("Button {} on the second page is selected.".format(button_id))
        global Diffcality
        Diffcality=button_id
        self.current_page = 3
        play_game()
      

 def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

 def run(self):
        self.window.mainloop()


# Function to handle a button click
def handle_click(row, col):
    pass #empty

# Function to make the AI player's move
def make_ai_move_With_Beta():

    global current_player
    if sum(sum(row) for row in board) == 0:
        # Make random first move
        col = random.randint(0, BOARD_COLS - 1)
        row = get_next_row(col)
     
    else:
        best_move = get_best_move_With_Beta()
        if best_move:
            row, col = best_move
    board[row][col] = current_player
    buttons[row][col].config(state="disabled")
    buttons[row][col].config(bg="blue" if current_player == BLUE else "red")
    current_player = RED if current_player == BLUE else BLUE
    root.update()
    time.sleep(2)


# Function to check if a player has won
def check_winner(player):
    # Check rows
    for row in range(6):
        for col in range(4):
            if (
                board[row][col] == player and
                board[row][col + 1] == player and
                board[row][col + 2] == player and
                board[row][col + 3] == player
            ):
                return True

    # Check columns
    for col in range(7):
        for row in range(3):
            if (
                board[row][col] == player and
                board[row + 1][col] == player and
                board[row + 2][col] == player and
                board[row + 3][col] == player
            ):
                return True

    # Check diagonals (top left to bottom right)
    for row in range(3):
        for col in range(4):
            if (
                board[row][col] == player and
                board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player
            ):
                return True

    # Check diagonals (top right to bottom left)
    for row in range(3):
        for col in range(3, 7):
            if (
                board[row][col] == player and
                board[row + 1][col - 1] == player and
                board[row + 2][col - 2] == player and
                board[row + 3][col - 3] == player
            ):
                return True

    return False

# Function to check if there are any moves left
def is_moves_left():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == EMPTY:
                return True
    return False

# Function to get the best move for the AI player
def get_best_move_With_Beta():
    best_score = float("-inf")
    best_move = None

    for col in range(BOARD_COLS):
        if is_valid_move(col):
            row = get_next_row(col)
            board[row][col] = RED
            score = minimax_With_Beta(board, Diffcality-1, float("-inf"), float("inf"), False)
            board[row][col] = EMPTY

            if score > best_score:
                best_score = score
                best_move = (row, col)

    return best_move

# Function to determine if a move is valid
def is_valid_move(col):
    return board[0][col] == EMPTY

# Function to get the next available row in a column
def get_next_row(col):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None

# Minimax algorithm with alpha-beta pruning
def minimax_With_Beta(board, depth, alpha, beta, maximizing_player):
    scores = {
        BLUE: -100,
        RED: 100,
        "tie": 0
    }

    if check_winner(BLUE):
        return scores[BLUE]
    if check_winner(RED):
        return scores[RED]
    if not is_moves_left():
        return scores["tie"]

    if depth == 0:
        return evaluate_board(board)

    if maximizing_player:
        max_score = float("-inf")
        for col in range(BOARD_COLS):
            if is_valid_move(col):
                row = get_next_row(col)
                board[row][col] = RED
                score = minimax_With_Beta(board, depth - 1, alpha, beta, False)
                board[row][col] = EMPTY
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
        return max_score
    else:
        min_score = float("inf")
        for col in range(BOARD_COLS):
            if is_valid_move(col):
                row = get_next_row(col)
                board[row][col] = BLUE
                score = minimax_With_Beta(board, depth - 1, alpha, beta, True)
                board[row][col] = EMPTY
                min_score = min(min_score, score)
                beta = min(beta, score)
                if alpha >= beta:
                    break
        return min_score

# Function to evaluate the current state of the board
def evaluate_board(board):
    score = 0

    # Check rows
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            window = board[row][col:col + 4]
            score += evaluate_window(window)
    
    # Check columns
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window)
    
    # Check diagonal (top left to bottom right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window)
    
    # Check diagonal (top right to bottom left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            window = [board[row + i][col - i] for i in range(4)]
            score += evaluate_window(window)
    
    return score

# Function to evaluate a window of 4 cells
def evaluate_window(window):
    score = 0
    blue_count = window.count(BLUE)
    red_count = window.count(RED)
    empty_count = window.count(EMPTY)

    if blue_count == 4:
        score += 100
    elif blue_count == 3 and empty_count == 1:
        score += 5
    elif blue_count == 2 and empty_count == 2:
        score += 2

    if red_count == 3 and empty_count == 1:
        score -= 4

    return score
#########################################################################################################################
def make_ai_move():
    global current_player
    if sum(sum(row) for row in board) == 0:
        # Make random first move
        col = random.randint(0, BOARD_COLS - 1)
        row = get_next_row(col)
    else:    
     best_move = get_best_move()
     if best_move:
        row, col = best_move
    board[row][col] = current_player
    buttons[row][col].config(state="disabled")
    buttons[row][col].config(bg="blue" if current_player == BLUE else "red")
    current_player = RED if current_player == BLUE else BLUE
    root.update()
    time.sleep(2)

# Function to get the best move for the AI player
def get_best_move():
    best_score = float("-inf")
    best_move = None

    for col in range(BOARD_COLS):
        if is_valid_move(col):
            row = get_next_row(col)
            board[row][col] = RED
            score = minimax(board, Diffcality, False)
            board[row][col] = EMPTY

            if score > best_score:
                best_score = score
                best_move = (row, col)

    return best_move




# Minimax algorithm
def minimax(board, depth, is_maximizing_player):
    scores = {
        BLUE: -100,
        RED: 100,
        "tie": 0
    }

    if check_winner(BLUE):
        return scores[BLUE]
    if check_winner(RED):
        return scores[RED]
    if not is_moves_left():
        return scores["tie"]

    if depth == 0:
        return evaluate_board(board)
    if is_maximizing_player:
        max_score = float('-inf')
        for col in range(BOARD_COLS):
            if is_valid_move(col):
                row = get_next_row(col)
                board[row][col] = RED
                score = minimax(board, depth - 1, False)
                board[row][col] = EMPTY
                max_score = max(score, max_score)
        return max_score
    else:
        min_score = float('inf')
        for col in range(BOARD_COLS):
            if is_valid_move(col):
                row = get_next_row(col)
                board[row][col] = BLUE
                score = minimax(board, depth - 1, True)
                board[row][col] = EMPTY
                min_score = min(score, min_score)
        return min_score

#########################################################################################################################
# Function to show a message box
def show_message(message):
    messagebox.showinfo("Game Over", message)

# Function to reset the game
def reset_game():
    global board, current_player
    board = [[EMPTY] * BOARD_COLS for _ in range(BOARD_ROWS)]
    current_player = BLUE
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            buttons[row][col].config(state=tk.NORMAL, bg="white")


def play_game():
    while is_moves_left() and not check_winner(current_player):
        if Algo==1:
            make_ai_move()
        elif Algo==2:
            make_ai_move_With_Beta()
    if not is_moves_left() and not check_winner(current_player):
        show_message("It's a tie!")
        reset_game()
    elif check_winner(current_player):
        show_message("Player {} wins!".format("Blue" if current_player == BLUE else "Red"))
        reset_game()

# Create the buttons and associate the click handler
for i in range(BOARD_ROWS):
    row_buttons = []
    for j in range(BOARD_COLS):
        button = tk.Button(root, width=5, height=2, bg="white", command=lambda row=i, col=j: handle_click(row, col))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Start the game

gui = GUI()
gui.run()  


# Run the main loop
root.mainloop()