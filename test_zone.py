import statistics

import Tictacto as ti
import minMax_AI_Tictac as minMax
from modules.utils import *
import copy
import json
from json.decoder import JSONDecodeError
from collections import deque

moves_done = 0
elapse = []

def are_boards_mirrored(board1, board2):
    size = len(board1)
    return all(board1[i][j] == board2[j][i] for i in range(size) for j in range(size))


def get_key(board):
    return ''.join([''.join(row) for row in board])


def create_data_structure(key:str, board:list[list[str]], depth: int, amount_to_win: int, point_of_the_board:int, player_token: str):
    """
    How the data will look like in the JSON file
    :param key: name of the variable
    :param board: how the board look like
    :param depth: the amounf of turn played
    :param amount_to_win: how much case we need to win
    :param point_of_the_board: the worth of the board for the player
    :return:
    """
    t = {
        key: {
            "Board": board if ''.join([''.join(row) for row in board]).strip() else [],
            "Depth": depth,
            "Winning": ti.three_case_winning(board, amount_to_win)[0],
            "Player": player_token,
            "point of the move": point_of_the_board,
        }
    }
    return t if all(t) else None


def get_mirrored_versions(board):
    size = len(board)
    mirrored_versions = []

    # 90 degrees rotation
    rotated_90 = [[board[size - j - 1][i] for j in range(size)] for i in range(size)]
    mirrored_versions.append(rotated_90)

    # 180 degrees rotation
    rotated_180 = [[board[size - i - 1][size - j - 1] for j in range(size)] for i in range(size)]
    mirrored_versions.append(rotated_180)

    # 270 degrees rotation
    rotated_270 = [[board[j][size - i - 1] for j in range(size)] for i in range(size)]
    mirrored_versions.append(rotated_270)

    # Horizontal reflection
    horizontal_reflection = [[board[i][size - j - 1] for j in range(size)] for i in range(size)]
    mirrored_versions.append(horizontal_reflection)

    # Vertical reflection
    vertical_reflection = [[board[size - i - 1][j] for j in range(size)] for i in range(size)]
    mirrored_versions.append(vertical_reflection)

    # Diagonal reflection (main diagonal)
    diagonal_reflection_main = [[board[j][i] for j in range(size)] for i in range(size)]
    mirrored_versions.append(diagonal_reflection_main)

    # Diagonal reflection (counter-diagonal)
    diagonal_reflection_counter = [[board[size - j - 1][size - i - 1] for j in range(size)] for i in range(size)]
    mirrored_versions.append(diagonal_reflection_counter)

    return mirrored_versions


def check_memo(board, memo):
    board_key = get_key(board)
    mirrored_versions = get_mirrored_versions(board)
    mirrored_keys = [get_key(mirrored_board) for mirrored_board in mirrored_versions]

    existing_key = None
    for key in [board_key] + mirrored_keys:
        if key in memo:
            existing_key = key
            break

    return board_key, existing_key


def prepare_next_move(board, move, player_key, player_token, memo, amount_to_win):
    next_board = minMax.give_board_new_tile(board, move[0], move[1], player_token[player_key])
    next_player_key = 2 if player_key == 1 else 1

    # Memoization logic
    next_board_key = get_key(next_board)
    if next_board_key in memo:
        next_board_worth = memo[next_board_key]["point of the move"]  # Changed this line
    else:
        next_board_worth = calculate_board_worth_for_player(player_token, player_key, next_board, amount_to_win, ' ', 1, 20, 15, 7, 5)

    return next_board, next_board_worth, next_player_key



def update_progress(moves_done, max_depth, total_possibilities):

    r = "\\", "|", "/", "-"
    expected_move_still_needed = total_possibilities - moves_done

    if not elapse:  # Check if elapse is empty
        t = 0
    else:
        t = (statistics.median(elapse) * expected_move_still_needed)

    clear_screen()
    print(f'{r[moves_done % 4]} calculating expected time , expected_move_still_needed ')
    return moves_done / max_depth



def calculate_board_worth_for_player(memo: dict, players_tokens: dict[int:dict], evaluating_player: int, board: list[list[str]], distance_to_win: int,
                                     empty_cell: str, value_empty: int, value_to_win: int, value_to_block_win: int,
                                     value_towards_win: int, value_towards_blocking_win: int) -> int:

    board_key = get_key(board)

    if board_key in memo:
        return memo[board_key]

    points: int = 0
    total_worth_array = ti.board_creation(len(board))
    for e, row in enumerate(board):
        for k, col in enumerate(row):
            surrouding_cells = minMax.get_directional_neighbors(board, e, k, distance_to_win)
            cell_worth = minMax.surrounding_evaluation(surrouding_cells, players_tokens, evaluating_player, empty_cell,
                           value_empty, value_to_win, value_to_block_win, value_towards_win,value_towards_blocking_win,
                                                       distance_to_win, board, [e, k])
            total_worth_array[e][k] = cell_worth
    for e in total_worth_array:
        for k in e:
            points = k + points

    memo[board_key] = points
    return points


def count_possibilities_helper(args):
    return count_possibilities(*args)


def count_possibilities(board, current_depth, max_depth, amount_to_win, players_token, player_key):
    if players_token[player_key]['amount played'] >= amount_to_win:
        if current_depth >= max_depth or ti.three_case_winning(board, amount_to_win)[0]:
            return 1

    max_possible_depth = len(board) * len(board[0]) - current_depth
    if max_depth > max_possible_depth:
        max_depth = max_possible_depth

    next_possible_moves = minMax.generate_moves(board)

    next_boards_and_keys = []
    for move in next_possible_moves:
        next_board = minMax.give_board_new_tile(board, move[0], move[1], players_token[player_key]['token'])
        next_player_key = 2 if player_key == 1 else 1
        next_boards_and_keys.append((next_board, current_depth + 1, max_depth, amount_to_win, players_token, next_player_key))

    results = []
    for args in next_boards_and_keys:
        result = count_possibilities_helper(args)
        results.append(result)

    return sum(results)


# ---------------------------- OPTIMISATION ZONE ------------------------------------------------

# Previous version :
'''
def generate_json_data(board: list[list[str]], current_depth: int, max_depth: int, amount_to_win: int, player_token: dict, player_key: int, point_of_board: int, memo: dict = {}, path: str = "") -> dict:
    global moves_done
    global elapse

    board_key, existing_key = check_memo(board, memo)

    if existing_key is not None:
        return {"ref": memo[existing_key]["path"]}

    key = f"Depth {current_depth}"
    data_structure = create_data_structure(key, board, current_depth, amount_to_win, point_of_board)

    if current_depth >= max_depth or data_structure[key]["Winning"]:
        return data_structure

    next_possible_moves = minMax.generate_moves(board)
    option_count = 0

    for move in next_possible_moves:
        tic = time.perf_counter()
        option_name = f"Option {option_count}"
        next_board, next_board_worth, next_player_key = prepare_next_move(board, move, player_key, player_token, memo, amount_to_win)

        next_move_data = generate_json_data(
            next_board, current_depth + 1, max_depth, amount_to_win, player_token, next_player_key, next_board_worth, memo, path=f"{path}/{key}/Next Possible Move/{option_name}")
        data_structure[key]["Next Possible Move"][option_name] = next_move_data
        option_count += 1

        moves_done += 1
        progress = update_progress(moves_done, max_depth, board)

        toc = time.perf_counter()
        elapse.append(toc - tic)

    data_structure["path"] = path
    memo[board_key] = data_structure
    return data_structure
'''
'''

# TODO: NEED FULL REDONE
# TODO : CAN'T SAVE DATA ANYMORE EXCEPT ONE AND INCORRECT
def generate_json_data(board: list[list[str]], current_depth: int, max_depth: int, amount_to_win: int, player_token: dict, player_key: int, point_of_board: int, memo: dict = {}, path: str = "") -> dict:
    global moves_done
    global elapse

    board_key, existing_key = check_memo(board, memo)

    if existing_key is not None:
        return {"ref": existing_key}

    key = f"{board_key}"
    data_structure = create_data_structure(key, board, current_depth, amount_to_win, point_of_board, player_token[player_key]['token'])

    if current_depth >= max_depth or data_structure[key]["Winning"]:
        memo[key] = data_structure[key]
        return {"ref": key}

    next_possible_moves = minMax.generate_moves(board)
    option_count = 0

    for move in next_possible_moves:
        tic = time.perf_counter()
        option_name = f"Option {option_count}"
        next_board, next_board_worth, next_player_key = prepare_next_move(board, move, player_key, player_token, memo, amount_to_win)

        next_move_data = generate_json_data(
            next_board, current_depth + 1, max_depth, amount_to_win, player_token, next_player_key, next_board_worth, memo, path=f"{path}/{key}/Next Possible Move/{option_name}")
        data_structure[key]["Next Possible Move"][option_name] = next_move_data
        option_count += 1

        moves_done += 1

        toc = time.perf_counter()
        elapse.append(toc - tic)

    data_structure["path"] = path
    memo[key] = data_structure[key]
    return {"ref": key}
'''



# --------------------------------------------------------------------------------------------


# -------------------------------- OPTIMISE TO REPLACE ZONE ----------------------------------

def calculate_board_worth(board: list[list[str]], amount_to_win: int, player_token: dict, player_key: int) -> int:
    total_board_worth: int = 0
    for e, row in enumerate(board):
        for k, cell in enumerate(row):
            total_board_worth += minMax.surrounding_evaluation(
                minMax.get_directional_neighbors(board, e, k, amount_to_win), player_token, player_key, ' ',
                1, 20, 15, 7, 4, amount_to_win, board, [e, k])  # Calculate the worth of a specific board
    return total_board_worth




def board_to_tuple(board):
    return tuple(tuple(row) for row in board)

def generate_json_data(board: list[list[str]], depth: int, amount_to_win: int, player_token: dict, player_key: int,
                       id: int) -> None:
    global moves_done
    global elapse
    board_data = deque([board])
    actual_depth = 0
    filename = f'{len(board)}x{len(board)}.json'
    processed_boards = set()

    # Read the existing data from the file
    try:
        with open(filename, 'r') as infile:
            existing_data = json.load(infile)
    except FileNotFoundError:
        existing_data = {}
    except JSONDecodeError:
        print(f'Error: The JSON file {filename} is broken. Skipping this file.')
        existing_data = {}

    while depth > 0:
        for _ in range(len(board_data)):
            depth_board = board_data.popleft()
            all_possible_move = minMax.generate_moves(board)

            # Calculation for one depth
            for row, cell in all_possible_move:
                board_copy = copy.deepcopy(depth_board)
                board_copy[row][cell] = player_token[player_key]["token"]

                board_tuple = board_to_tuple(board_copy)
                mirrored_board_tuples = [board_tuple] + [board_to_tuple(b) for b in get_mirrored_versions(board_copy)]

                # Check if the board or its mirrored version has been processed
                if any(b in processed_boards for b in mirrored_board_tuples):
                    continue

                board_worth = calculate_board_worth(board_copy, amount_to_win, player_token, player_key)  # Give how much the board worth

                json_data = create_data_structure(str(id), board_copy, actual_depth, amount_to_win, board_worth, player_token[player_key]["token"]) # Format the data

                # Combine the existing data with the new data
                key = list(json_data.keys())[0]  # Get the key of the current data dictionary
                existing_data[key] = json_data[key]  # Add the current data to the existing data using the key

                if not json_data[str(id)]["Winning"]:
                    board_data.append(board_copy)

                # Mark the board as processed
                processed_boards.add(board_tuple)

                id += 1

        actual_depth += 1
        player_key += 1
        if player_key > len(player_token):
            player_key = 1
        depth -= 1

    # Save the updated data back to the file
    with open(filename, 'w') as outfile:
        json.dump(existing_data, outfile, indent=4)
    print(f'Saving we are at : {id}')







#--------------------------------------------------------------------------------------------


from multiprocessing.pool import ThreadPool


def main():
    size = 5
    amount_to_win = 3
    players_token = {1: {'token': 'X', 'amount played': 0}, 2: {'token': 'O', 'amount played': 0}}
    player_key = 1
    board = ti.board_creation(size)
    max_depth = 4
    first_id = 0
    generate_json_data(board, max_depth, amount_to_win, players_token, player_key, first_id)





if __name__ == '__main__':
    main()




# surounding evaluation :

