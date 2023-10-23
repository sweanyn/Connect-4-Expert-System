import json
import sys
import numpy as np

# CONSTANTS
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_SIZE = 4
OFFSET = WINDOW_SIZE - 1
EMPTY = 0
SWAP_PLAYER = 3

# SET THIS FOR ALPHA-BETA SEARCH DEPTH
ALPHA_BETA_DEPTH_LIMIT = 4




def is_valid_move(grid, col):
    return grid[0, col] == 0

def get_valid_moves(grid):
    valid_moves = []
    for col in range(COLUMN_COUNT):
        if is_valid_move(grid, col):
            valid_moves.append(col)
    return valid_moves

def make_move(grid, col, player):
    # IMPORTANT: Make sure to always .copy() the 'grid' when calling 'make_move()'
    for row in range(ROW_COUNT-1, -1, -1):
        if grid[row, col] == 0:
            grid[row, col] = player
            break
    return grid

def is_end_of_game(grid, player): # Winning move / game end.
    # Checking horizontal locations for win
    for col in range(COLUMN_COUNT-3):
        for row in range (ROW_COUNT):
            if (grid[row, col]   == player and 
                grid[row, col+1] == player and 
                grid[row, col+2] == player and 
                grid[row, col+3] == player):
                return True
    
    # Checking vertical locations for win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if (grid[row, col]   == player and 
                grid[row+1, col] == player and 
                grid[row+2, col] == player and 
                grid[row+3, col] == player):
                return True
            
    # Checking positive sloped diaganols for win
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if (grid[row, col]     == player and 
                grid[row+1, col+1] == player and 
                grid[row+2, col+2] == player and 
                grid[row+3, col+3] == player):
                return True
            
    # Checking negatively sloped diaganols for win
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if (grid[row, col]     == player and 
                grid[row-1, col+1] == player and 
                grid[row-2, col+2] == player and 
                grid[row-3, col+3] == player):
                return True

    # Checking for a draw here
    return 0 not in grid[0, :]

def score_heuristic(grid, player):
    score = 0
    # Evaluate the board for the given player
    # Placeholder that just returns 0
    # Scoring Vertical Columns (Checking Window Sizes for how many pieces are 'player')
    # Score Vertical
    for col in range(COLUMN_COUNT):  
        for row in range(ROW_COUNT - OFFSET):
            window = grid[row:row+WINDOW_SIZE, col]
            if np.count_nonzero(window == player) == 4:
                score += 100
            elif np.count_nonzero(window == player) == 3 and np.count_nonzero(window == EMPTY) == 1:
                score += 10

    # Score Horizontal
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - OFFSET):  
            window = grid[row, col:col+WINDOW_SIZE]
            if np.count_nonzero(window == player) == 4:
                score += 100
            elif np.count_nonzero(window == player) == 3 and np.count_nonzero(window == EMPTY) == 1:
                score += 10




    return score

def alphabeta(grid, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or is_end_of_game(grid, player) or is_end_of_game(grid, SWAP_PLAYER-player):
        return score_heuristic(grid, player)

    if maximizing_player:
        max_score = float('-inf')
        for col in range(COLUMN_COUNT):
            if is_valid_move(grid, col):
                new_grid = make_move(grid.copy(), col, player) # Ensuring to make a deep copy of the grid.
                score = alphabeta(new_grid, depth-1, alpha, beta, False, SWAP_PLAYER-player)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return max_score
    else:
        min_score = float('inf')
        for col in range(COLUMN_COUNT):
            if is_valid_move(grid, col):
                new_grid = make_move(grid.copy(), col, player) # Ensuring to make a deep copy of the grid.
                score = alphabeta(new_grid, depth-1, alpha, beta, True, SWAP_PLAYER-player)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return min_score

def find_best_move(grid, player):
    best_score = float('-inf')
    best_col = -1
    valid_moves = get_valid_moves(grid) # A list of all the possible moves we can make.
    for col in valid_moves:
        new_grid = make_move(grid.copy(), col, player) # Deep copy the grid.
        move_score = alphabeta(new_grid, ALPHA_BETA_DEPTH_LIMIT, float('-inf'), float('inf'), False, SWAP_PLAYER-player)
        if move_score > best_score:
            best_score = move_score
            best_col = col
    return best_col

def main():
    print('Connect Four with Alpha-Beta Pruning in Python', file=sys.stderr)
    for line in sys.stdin:
        print(line, file=sys.stderr)
        
        json_data = json.loads(line)
        
        grid = np.array(json_data["grid"], dtype=int)

        move = find_best_move(grid, json_data["player"])
        
        action = {"move": move}
        
        action_json = json.dumps(action)

        print(action_json, file=sys.stderr)
        print(action_json, flush=True)

if __name__ == '__main__':
    main()