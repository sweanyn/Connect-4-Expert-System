'''
BY: Nathan Sweany
University of Colorado Denver, Fall 2023 - Introduction to AI (CSCI 4202)
Professor Doug Williams
Heavily Adapted from: https://github.com/KeithGalli/Connect4-Python
'''

import json
import sys
import numpy as np

# CONSTANTS
WINDOW_SIZE = 4
OFFSET = WINDOW_SIZE - 1
EMPTY = 0
SWAP_PLAYER = 3
CENTER_COLUMN_MULTIPLIER = 3
# SET THIS FOR ALPHA-BETA SEARCH DEPTH
ALPHA_BETA_DEPTH_LIMIT = 6

def is_valid_move(grid, col): 
    # Returns whether or not there is space in the given column (T/F).
    return grid[0, col] == EMPTY

def get_valid_moves(grid): 
    # Returns a list of the current available moves for the player to choose.
    valid_moves = []
    for col in range(COLUMN_COUNT):
        if is_valid_move(grid, col):
            valid_moves.append(col)
    return valid_moves

def make_move(grid, col, player):
    # IMPORTANT: Make sure to always .copy() the 'grid' when calling 'make_move()'
    for row in reversed(range(ROW_COUNT)):
        if grid[row, col] == 0:
            grid[row, col] = player
            break
    return grid

def is_end_of_game(grid, player): # Winning move / game end.
    # Checking horizontal locations for win
    for col in range(COLUMN_COUNT-OFFSET):
        for row in range (ROW_COUNT):
            if (grid[row, col]   == player and 
                grid[row, col+1] == player and 
                grid[row, col+2] == player and 
                grid[row, col+3] == player):
                return True
    
    # Checking vertical locations for win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-OFFSET):
            if (grid[row, col]   == player and 
                grid[row+1, col] == player and 
                grid[row+2, col] == player and 
                grid[row+3, col] == player):
                return True
            
    # Checking positive sloped diaganols for win
    for col in range(COLUMN_COUNT-OFFSET):
        for row in range(ROW_COUNT-OFFSET):
            if (grid[row, col]     == player and 
                grid[row+1, col+1] == player and 
                grid[row+2, col+2] == player and 
                grid[row+3, col+3] == player):
                return True
            
    # Checking negatively sloped diaganols for win
    for col in range(COLUMN_COUNT-OFFSET):
        for row in range(OFFSET, ROW_COUNT):
            if (grid[row, col]     == player and 
                grid[row-1, col+1] == player and 
                grid[row-2, col+2] == player and 
                grid[row-3, col+3] == player):
                return True
    return False # If the function hasn't returned by now, the game hasn't ended due to a win.

def is_draw(grid):
    # Returns whether or not there are spaces left to play in the board (T/F).
    return 0 not in grid[0, :]

def score_window(window, player):
    score = 0
    opp_player = PLAYER
    if player == PLAYER:
        opp_player = OPP_PLAYER
    
    # Scoring self-moves
    if list(window).count(player) == 4:
        score += 10
    if list(window).count(player) == 3 and list(window).count(EMPTY) == 1:
        score += 5
    if list(window).count(player) == 2 and list(window).count(EMPTY) == 2:
        score += 2
    # Blocking (Scoring opp-moves)
    if list(window).count(opp_player) == 3 and list(window).count(EMPTY) == 1:
        score -= 4
    return score

def score_heuristic(grid, player):
    score = 0
    # Evaluate the board for the given player

    # Score Center column
    center_array = [int(i) for i in list(grid[:, CENTER_COLUMN])]
    center_column_count = center_array.count(player)
    score += center_column_count * CENTER_COLUMN_MULTIPLIER

    # Score Horizontal
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - OFFSET):  
            window = grid[row, col:col+WINDOW_SIZE]
            score += score_window(window, player)

    # Score Vertical
    for col in range(COLUMN_COUNT):  
        for row in range(ROW_COUNT - OFFSET):
            window = grid[row:row+WINDOW_SIZE, col]
            score += score_window(window, player)

    # Score Positive Slope Diagonal
    for row in range(ROW_COUNT - OFFSET):
        for col in range(COLUMN_COUNT - OFFSET):
            window = [grid[row+i, col+i] for i in range(WINDOW_SIZE)]
            score += score_window(window, player)

    # Score Negative Slope Diagonal
    for row in range(ROW_COUNT - OFFSET):
        for col in range(OFFSET, COLUMN_COUNT):
            window = [grid[row+i, col-i] for i in range(WINDOW_SIZE)]
            score += score_window(window, player)   
    return score

def alphabeta(grid, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return(None, score_heuristic(grid, PLAYER))
    if is_end_of_game(grid, PLAYER):
        return(None, 1000000) # Player Win
    if is_end_of_game(grid, OPP_PLAYER):
        return(None, -1000000) # Opponent Win
    if is_draw(grid):
        return (None, 0) # Draw
    if len(get_valid_moves(grid)) == 0:
        return(None, 0) # Board is full == Draw

    if maximizing_player:
        max_score = float('-inf')
        for col in range(COLUMN_COUNT):
            if is_valid_move(grid, col):
                new_grid = make_move(grid.copy(), col, PLAYER) # Ensuring to make a deep copy of the grid.
                _, new_score = alphabeta(new_grid, depth-1, alpha, beta, False)         
                if new_score > max_score:
                    max_score = new_score
                    column = col
                alpha = max(alpha, new_score)
                if alpha >= beta:
                    break
        return column, max_score
    else: # Minimizing player
        min_score = float('inf')
        for col in range(COLUMN_COUNT):
            if is_valid_move(grid, col):
                new_grid = make_move(grid.copy(), col, OPP_PLAYER) # Ensuring to make a deep copy of the grid.
                _, new_score = alphabeta(new_grid, depth-1, alpha, beta, True)
                if new_score < min_score:
                    min_score = new_score
                    column = col
                beta = min(beta, new_score)
                if alpha >= beta:
                    break
        return column, min_score

def main():
    print('Connect Four with Alpha-Beta Pruning in Python', file=sys.stderr)
    for line in sys.stdin:
        print(line, file=sys.stderr)
        json_data = json.loads(line)
        # Setting global variables based on read data (to allow for multiple grid-sizes)
        global ROW_COUNT 
        ROW_COUNT = int(json_data["height"])
        global COLUMN_COUNT
        COLUMN_COUNT = int(json_data["width"])
        global CENTER_COLUMN
        CENTER_COLUMN = COLUMN_COUNT // 2
        global PLAYER
        PLAYER = int(json_data["player"])
        global OPP_PLAYER
        OPP_PLAYER = SWAP_PLAYER - PLAYER
        grid = np.array(json_data["grid"], dtype=int).T # Transpose to get out of column-major format.
        move, _ = alphabeta(grid, ALPHA_BETA_DEPTH_LIMIT, float('-inf'), float('inf'), True)
        action = {"move": move}
        action_json = json.dumps(action)
        print(action_json, file=sys.stderr)
        print(action_json, flush=True)

if __name__ == '__main__':
    main()