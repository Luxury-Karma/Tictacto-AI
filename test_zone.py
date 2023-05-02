import json
import Tictacto as ti
import minMax_AI_Tictac as minMax

def get_key(board):
    return ''.join([''.join(row) for row in board])
def create_data_structure(key, board, depth, amount_to_win):
    return {
        key: {
            "Board": f"{board}",
            "Depth": f"{depth}",
            "Winning": ti.three_case_winning(board, amount_to_win)[0],
            "Next Possible Move": {}
        }
    }



def generate_json_data(board, current_depth, max_depth, amount_to_win, player_token, player_key):
    key = f"Depth {current_depth}"
    data_structure = create_data_structure(key, board, current_depth, amount_to_win)

    if current_depth >= max_depth or data_structure[key]["Winning"]:
        return data_structure

    next_possible_moves = minMax.generate_moves(board)
    option_count = 0

    for move in next_possible_moves:
        next_board = minMax.give_board_new_tile(board, move[0], move[1], player_token[player_key])
        option_name = f"Option {option_count}"
        next_player_key = 2 if player_key == 1 else 1
        next_move_data = generate_json_data(
            next_board, current_depth + 1, max_depth, amount_to_win, player_token, next_player_key
        )
        data_structure[key]["Next Possible Move"][option_name] = next_move_data[list(next_move_data.keys())[0]]
        option_count += 1

    return data_structure




def main():
    size = 5
    amount_to_win = 3
    players_token = {1: 'X', 2: 'O'}
    player_key = 1
    board = ti.board_creation(size)
    max_depth = 20
    data_structure = generate_json_data(board, 1, max_depth, amount_to_win, players_token, player_key)

    with open('tic_tac_toe_data.json', 'w') as outfile:
        json.dump(data_structure, outfile, indent=4)

if __name__ == '__main__':
    main()

