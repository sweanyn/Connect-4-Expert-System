import json
import sys
import subprocess
import time

def display_options(valid_moves):
    print("Available Moves:", ", ".join(map(str, valid_moves)), file=sys.stderr)

def get_player_move(valid_moves):
    while True:
        # Run input_script.py in a new terminal
        subprocess.Popen(['cmd.exe', '/c', 'start', 'cmd', '/k', 'python USER_INPUT_SCRIPT.py & exit'])
        
        # Wait for a few seconds to make sure the input has been captured
        time.sleep(10)
        
        # Read the user's move from the temp file
        with open("temp_input.txt", "r") as file:
            move = int(file.read().strip())
        
        if move in valid_moves:
            return move
        else:
            print(f"Invalid move. Choose from {valid_moves}")

def valid_moves(precept):
    grid = precept["grid"]
    moves = [i for i, col in enumerate(grid) if col[0] == 0]
    return moves

def main():
    print('Connect Four in Python', file=sys.stderr)
    for line in sys.stdin:
        precept = json.loads(line)
        valid_move_positions = valid_moves(precept)
        display_options(valid_move_positions)
        chosen_move = get_player_move(valid_move_positions)
        
        action = {"move": chosen_move}
        action_json = json.dumps(action)
        print(action_json, file=sys.stderr)
        print(action_json, flush=True)

if __name__ == '__main__':
    main()
