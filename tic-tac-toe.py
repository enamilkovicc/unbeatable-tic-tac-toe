import math
import tkinter as tk
import random

def initialize_game():
    """
    Initialize or reset the game state.
    """
    global board, buttons, current_player, is_empty_grid
    board = [[" " for _ in range(3)] for _ in range(3)]
    is_empty_grid = True
    current_player = "X"

def reset_game():
    """
    Reset the board and update UI.
    """
    initialize_game()
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state=tk.NORMAL, bg="#ade8f4")
    status_label.config(text="")
    ai_start_button.config(state=tk.NORMAL)

def handle_click(row, col):
    """
    Handle player's move, check winner, and switch turns.
    """
    global current_player, is_empty_grid

    if board[row][col] != " ":
        return

    board[row][col] = current_player
    buttons[row][col].config(text=current_player)

    winner, winning_positions = check_winner(board)
    if winner:
        end_game(winner, winning_positions)
        return

    current_player = "O" if current_player == "X" else "X"
    is_empty_grid = False
    ai_start_button.config(state=tk.DISABLED)

    if current_player == "O":
        root.after(300, ai_move)  # Small delay for better UX

def ai_move():
    """
    Execute AI's best move and check for winner.
    """
    global current_player
    move = best_move(board)
    if move:
        board[move[0]][move[1]] = "O"
        buttons[move[0]][move[1]].config(text="O")

    winner, winning_positions = check_winner(board)
    if winner:
        end_game(winner, winning_positions)
        return

    current_player = "X"

def best_move(board):
    """
    Determine the AI's best move.
    """
    if is_empty_grid:
        empty_positions = [(i, j) for i in range(3) for j in range(3)]
        return random.choice(empty_positions)

    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Implement the minimax algorithm with alpha-beta pruning.
    """
    winner, _ = check_winner(board)
    if winner == "X":
        return -10 + depth
    if winner == "O":
        return 10 - depth
    if winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        return best_score
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        return best_score
        return best_score

def check_winner(board):
    """
    Check the current board for a winner or draw.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != " ":
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != " ":
            return board[0][i], [(0, i), (1, i), (2, i)]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2], [(0, 2), (1, 1), (2, 0)]

    for row in board:
        if " " in row:
            return None, []

    return "Draw", []

def draw_winning_line(winning_positions):
    """
    Highlight the winning line on the GUI.
    """
    for (i, j) in winning_positions:
        buttons[i][j].config(bg="#ff4500")

def end_game(winner, winning_positions):
    """
    Handle game-ending scenarios.
    """
    if winner == "Draw":
        status_label.config(text="It's a draw!")
    else:
        status_label.config(text=f"{winner} wins!")
        draw_winning_line(winning_positions)

    root.after(1500, reset_game)

def start_ai_first():
    """
    Start the game with AI making the first move.
    """
    global current_player
    current_player = "O"
    ai_move()
    ai_start_button.config(state=tk.DISABLED)

def main():
    """
    Main function to set up the GUI and initialize the game.
    """
    global board, buttons, current_player, root, status_label, ai_start_button, is_empty_grid
    initialize_game()

    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.configure(bg="#c0c0c0")
    root.geometry("500x500")
    root.resizable(False, False)

    status_label = tk.Label(root, text="", font=("Arial", 16), bg="#c0c0c0", fg="#03045e")
    status_label.pack(pady=10)

    container = tk.Frame(root, bg="#c0c0c0")
    container.pack(expand=True)

    buttons = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(container, text="", font=("Arial", 20), width=5, height=2,
                                      bg="#ade8f4", fg="#03045e", relief="flat",
                                      command=lambda row=i, col=j: handle_click(row, col))
            buttons[i][j].grid(row=i, column=j, padx=10, pady=10)

    button_frame = tk.Frame(root, bg="#c0c0c0")
    button_frame.pack(pady=20)

    reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 14), bg="#ade8f4", fg="#03045e", relief="flat",
                              command=reset_game, width=10)
    reset_button.pack(side="left", padx=18)

    ai_start_button = tk.Button(button_frame, text="AI Starts", font=("Arial", 14), bg="#ade8f4", fg="#03045e", relief="flat",
                                 command=start_ai_first, width=10)
    ai_start_button.pack(side="right", padx=18)

    root.mainloop()

if __name__ == "__main__":
    main()
