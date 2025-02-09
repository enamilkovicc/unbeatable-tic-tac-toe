# Tic Tac Toe - AI with Minimax Algorithm

This is a simple **Tic Tac Toe** game built using **Python and Tkinter**, where the AI opponent plays optimally using the **Minimax algorithm with Alpha-Beta pruning**.

## Features
- **Player vs AI** mode
- **AI uses Minimax** for optimal moves
- **Alpha-Beta Pruning** for efficiency
- **AI can start first** (with a random initial move)
- **Graphical UI** with Tkinter

## How the AI Works
The AI uses the **Minimax algorithm** to evaluate all possible moves and choose the best one. 

### **Minimax Algorithm**
1. **Recursive simulation** of all possible game states.
2. **Assign scores**:
   - **+10** → AI ("O") wins
   - **-10** → Player ("X") wins
   - **0** → Draw
3. **AI maximizes its score** while assuming the player plays optimally to minimize it.
4. **Alpha-Beta Pruning** cuts unnecessary branches to improve efficiency.

## How to Play
1. **Run the script**:  
   ```sh
   python tic_tac_toe.py

2. **Click a tile to place "X".**
3. **AI will respond with "O".**
4. **First to get 3 in a row wins!**
