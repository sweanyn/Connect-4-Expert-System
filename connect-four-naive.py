import json
import random
import sys

def valid_moves(precept):
    grid = precept["grid"]
    # moves = []
    # for i, col in enumerate(grid):
        # if col[0] == 0:
            # moves.append(i)
    moves = [i for i, col in enumerate(grid) if col[0] == 0]
    return moves

def main():
    print('Connect Four in Python', file=sys.stderr)
    for line in sys.stdin:
        print(line, file=sys.stderr)
        precept = json.loads(line)
        moves = valid_moves(precept)
        print(moves, file=sys.stderr)
        move = random.choice(moves)
        action = {"move": move}
        action_json = json.dumps(action)
        print(action_json, file=sys.stderr)
        print(action_json, flush=True)

if __name__ == '__main__':
    main()
