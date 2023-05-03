import json
import os
import statistics
import time

import Tictacto as ti
import minMax_AI_Tictac as minMax
import sys
from multiprocessing import Pool, Manager
from functools import partial
import math
from modules.utils import *
import datetime


moves_done = 0


def are_boards_mirrored(board1, board2):
    size = len(board1)
    return all(board1[i][j] == board2[j][i] for i in range(size) for j in range(size))


def get_key(board):
    return ''.join([''.join(row) for row in board])


def create_data_structure(key:str, board:list[list[str]], depth: int, amount_to_win: int, point_of_the_board:int):
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
            "point of the move": point_of_the_board,
            "Next Possible Move": {}
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


# TODO: REDOO ALL
def generate_json_data(board: list[list[str]], current_depth: int, max_depth: int, amount_to_win: int, player_token: dict, player_key: int, point_of_board: int, memo: dict = {}, path: str = "") -> dict:
    global moves_done
    global elapse
    # Check if the current board or any mirrored version already exists in the memo dictionary
    board_key = get_key(board)
    mirrored_versions = get_mirrored_versions(board)
    mirrored_keys = [get_key(mirrored_board) for mirrored_board in mirrored_versions]

    existing_key = None
    for key in [board_key] + mirrored_keys:
        if key in memo:
            existing_key = key
            break

    if existing_key is not None:
        return {"ref": memo[existing_key]["path"]}
    # Check if the current board already exists in the memo dictionary
    board_key = get_key(board)
    if board_key in memo:
        return {"ref": memo[board_key]["path"]}

    key = f"Depth {current_depth}"
    data_structure = create_data_structure(key, board, current_depth, amount_to_win, point_of_board)

    if current_depth >= max_depth or data_structure[key]["Winning"]:
        return data_structure

    next_possible_moves = minMax.generate_moves(board)
    option_count = 0
    progress = -1

    for move in next_possible_moves:
        tic = time.perf_counter()
        next_board = minMax.give_board_new_tile(board, move[0], move[1], player_token[player_key])
        option_name = f"Option {option_count}"
        next_player_key = 2 if player_key == 1 else 1

        # Memoization logic
        next_board_key = get_key(next_board)
        if next_board_key in memo:
            next_board_worth = memo[next_board_key][list(memo[next_board_key].keys())[0]]["point of the move"]
        else:
           next_board_worth = calculate_board_worth_for_player(player_token, player_key, next_board, amount_to_win, ' ', 1, 20, 15, 7, 5)

        next_move_data = generate_json_data(
            next_board, current_depth + 1, max_depth, amount_to_win, player_token, next_player_key, next_board_worth, memo, path=f"{path}/{key}/Next Possible Move/{option_name}")
        data_structure[key]["Next Possible Move"][option_name] = next_move_data
        option_count += 1


        moves_done += 1

        r = "\\","|","/","-"

        toc = time.perf_counter()
        elapse.append(toc-tic)
        expected_move_still_needed = (math.factorial(len(board) * len(board)) * max_depth) - moves_done
        t = (statistics.median(elapse)*expected_move_still_needed)

        clear_screen()
        print(f'{r[moves_done%4]} calculating expected time {str(t)},expected_move_still_needed{expected_move_still_needed}')
        #print(f'{elapse}')
    # Memoize the current data structure with its path before returning it
    data_structure["path"] = path
    memo[board_key] = data_structure
    return data_structure








def calculate_board_worth_for_player(players_tokens: dict[int:dict], evaluating_player: int, board: list[list[str]], distance_to_win: int,
                                     empty_cell: str, value_empty: int, value_to_win: int, value_to_block_win: int,
                                     value_towards_win: int, value_towards_blocking_win: int, memo: dict = {}) -> int:
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


def main():
    size = 2
    amount_to_win = 3
    players_token = {1: 'X', 2: 'O'}
    player_key = 1
    board = ti.board_creation(size)
    max_depth = 9
    board_worth = calculate_board_worth_for_player(players_token,player_key,board,amount_to_win, ' ', 1, 20, 15, 7, 5)

    # Use a shared memo dictionary to store results of completed tasks
    manager = Manager()
    memo = manager.dict()

    # Partially apply the function to make it suitable for parallel execution
    generate_json_data_with_memo = partial(generate_json_data, memo=memo)

    # Parallelize the execution using a process pool
    with Pool(processes=4) as pool:
        data_structure = pool.apply(generate_json_data_with_memo, (board, 0, max_depth, amount_to_win, players_token, player_key, board_worth))

    with open(f'{size}x{size}.json', 'w') as outfile:
        json.dump(data_structure, outfile, indent=4)

if __name__ == '__main__':
    main()

