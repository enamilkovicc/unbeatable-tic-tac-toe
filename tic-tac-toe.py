import math 
import tkinter as tk  # For creating the graphical user interface (GUI).
import random  # For AI's random initial move.

def check_winner(board):
    """
    Check the current board for a winner or draw.

    :param board: 2D list representing the Tic Tac Toe board.
    :return: A tuple containing the winner ('X', 'O', or 'Draw') and the positions forming the winning line.
    """
    for i in range(3):
        # Check rows.
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != " ":
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
        # Check columns.
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != " ":
            return board[0][i], [(0, i), (1, i), (2, i)]

    # Check diagonals for a winner.
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2], [(0, 2), (1, 1), (2, 0)]

    # Check for an ongoing game (if any empty space exists).
    for row in board:
        if " " in row:
            return None, []

    # If no winner and no empty space, the game is a draw.
    return "Draw", []

def draw_winning_line(winning_positions):
    """
    Highlight the winning line on the GUI.

    :param winning_positions: List of tuples representing the winning positions.
    """
    for (i, j) in winning_positions:
        buttons[i][j].config(bg="#ff4500")

def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Implement the minimax algorithm with alpha-beta pruning.

    :param board: Current board state.
    :param depth: Current depth in the game tree.
    :param is_maximizing: Boolean indicating whether the AI is maximizing or minimizing.
    :param alpha: Best value that the maximizing player can guarantee.
    :param beta: Best value that the minimizing player can guarantee.
    :return: Best score for the current player.
    """
    winner, _ = check_winner(board)  # Check if the game is over.
    if winner == "X":
        return -10 + depth  # Favor quicker losses for AI.
    if winner == "O":
        return 10 - depth  # Favor quicker wins for AI.
    if winner == "Draw":
        return 0  # Neutral score for a draw.

    if is_maximizing:
        best_score = -math.inf  # Initialize best score for maximizing player.
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"  # Simulate AI's move.
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "  # Undo the move.
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break  # Prune remaining branches.
        return best_score
    else:
        best_score = math.inf  # Initialize best score for minimizing player.
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"  # Simulate opponent's move.
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "  # Undo the move.
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break  # Prune remaining branches.
        return best_score

def best_move(board):
    """
    Determine the AI's best move using the minimax algorithm.

    :param board: Current board state.
    :return: Tuple (row, col) representing the best move.
    """
    if all(cell == " " for row in board for cell in row):
        # If the board is empty, pick a random move.
        empty_positions = [(i, j) for i in range(3) for j in range(3)]
        return random.choice(empty_positions)

    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"  # Simulate AI's move.
                score = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = " "  # Undo the move.
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def reset_game():
    """
    Reset the game board and GUI to its initial state.
    """
    global board, buttons, current_player, status_label, ai_start_button, is_empty_grid
    board = [[" " for _ in range(3)] for _ in range(3)]  # Clear the board.
    is_empty_grid = True  # Indicate the grid is empty.
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state=tk.NORMAL, bg="#ade8f4")  # Reset button states.
    current_player = "X"
    status_label.config(text="")  # Clear the status label text.
    ai_start_button.config(state=tk.NORMAL if is_empty_grid else tk.DISABLED)  # Enable/disable AI button.

def handle_click(row, col):
    """
    Handle player's move and update the game state.

    :param row: Row index of the clicked cell.
    :param col: Column index of the clicked cell.
    """
    global board, current_player, is_empty_grid
    if board[row][col] == " ":
        board[row][col] = current_player  # Update the board with the player's move.
        buttons[row][col].config(text=current_player)  # Update the button text.
        winner, winning_positions = check_winner(board)
        if winner:
            if winner == "Draw":
                status_label.config(text="It's a draw!")
            else:
                status_label.config(text=f"{winner} wins!")
                draw_winning_line(winning_positions)
            root.after(1500, reset_game)  # Delay reset for visual effect.
            return
        current_player = "O" if current_player == "X" else "X"  # Switch player.
        is_empty_grid = False  # Mark grid as non-empty.
        ai_start_button.config(state=tk.DISABLED)  # Disable AI button.
        if current_player == "O":
            ai_move()

def ai_move():
    """
    Execute AI's move and update the game state.
    """
    global board, current_player
    move = best_move(board)
    if move:
        board[move[0]][move[1]] = "O"  # Update board with AI's move.
        buttons[move[0]][move[1]].config(text="O")  # Update button text.
        winner, winning_positions = check_winner(board)
        if winner:
            if winner == "Draw":
                status_label.config(text="It's a draw!")
            else:
                status_label.config(text=f"{winner} wins!")
                draw_winning_line(winning_positions)
            root.after(1500, reset_game)  # Delay reset for visual effect.
            return
        current_player = "X"  # Switch turn back to player.

def start_ai_first():
    """
    Start the game with AI making the first move.
    """
    global current_player, ai_start_button
    current_player = "O"
    ai_move()
    ai_start_button.config(state=tk.DISABLED)  # Disable the AI start button.

def main():
    """
    Main function to set up the GUI and initialize the game.
    """
    global board, buttons, current_player, root, status_label, ai_start_button, is_empty_grid
    board = [[" " for _ in range(3)] for _ in range(3)]  # Initialize the board.
    is_empty_grid = True  # Indicate the grid is empty initially.
    current_player = "X"  # Set the starting player.

    root = tk.Tk()  # Create the main Tkinter window.
    root.title("Tic Tac Toe")  # Set the window title.
    root.configure(bg="#c0c0c0")  # Set the background color.
    root.geometry("500x500")  # Set the window size.
    root.resizable(False, False)  # Disable window resizing.

    # Status label to show the current game state.
    status_label = tk.Label(root, text="", font=("Arial", 16), bg="#c0c0c0", fg="#03045e")
    status_label.pack(pady=10)

    # Container frame for the game buttons.
    container = tk.Frame(root, bg="#c0c0c0")
    container.pack(expand=True)

    # Create buttons for the Tic Tac Toe grid.
    buttons = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(container, text="", font=("Arial", 20), width=5, height=2,
                                      bg="#ade8f4", fg="#03045e", relief="flat",
                                      command=lambda row=i, col=j: handle_click(row, col))
            buttons[i][j].grid(row=i, column=j, padx=10, pady=10)

    # Frame for additional control buttons.
    button_frame = tk.Frame(root, bg="#c0c0c0")
    button_frame.pack(pady=20)

    # Reset button to reset the game.
    reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 14), bg="#ade8f4", fg="#03045e", relief="flat",
                              command=reset_game, width=10)
    reset_button.pack(side="left", padx=18)

    # AI Starts button to let the AI make the first move.
    ai_start_button = tk.Button(button_frame, text="AI Starts", font=("Arial", 14), bg="#ade8f4", fg="#03045e", relief="flat",
                                 command=start_ai_first, width=10)
    ai_start_button.pack(side="right", padx=18)

    root.mainloop()

if __name__ == "__main__":
    main() 
