import copy

import Tictacto as ti
from typing import Dict, List, Tuple, Optional
from copy import deepcopy
import json


def get_directional_neighbors(matrix: List[List[str]], row: int, col: int, distance: int = 1) -> List[Tuple[int, int]]:
    neighbors = []

    for d_row in range(-distance, distance + 1):
        for d_col in range(-distance, distance + 1):
            if d_row == 0 and d_col == 0:
                continue

            new_row = row + d_row
            new_col = col + d_col

            if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]) and (
                    d_row == 0 or d_col == 0 or abs(d_row) == abs(d_col)):
                neighbors.append((new_row, new_col))

    return neighbors



def surrounding_evaluation(surrounding: List[Tuple[int, int]], players_token: Dict[int, str], active_player: int, empty_cell: str,
                           value_empty: int, value_to_win: int, value_to_block_win: int, value_towards_win: int,
                           value_towards_blocking_win: int, amount_to_win: int, board: List[List[str]],
                           position_on_the_board: List[int]) -> int:
    total_value = 0
    player = players_token[active_player]["token"]
    amount_of_cell = {value["token"]: 0 for key, value in players_token.items()}

    for coord in surrounding:
        e = board[coord[0]][coord[1]]
        if e == empty_cell:
            total_value += value_empty
        elif e == player:
            total_value += value_towards_win
            amount_of_cell[e] += 1
            if amount_of_cell[e] >= amount_to_win - 1:
                total_value += value_to_win
        else:
            total_value += value_to_block_win
            amount_of_cell[e] += 1
            if amount_of_cell[e] >= amount_to_win - 1:
                total_value += value_towards_blocking_win

    board_copy = copy.deepcopy(board)

    for _, value in players_token.items():
        actual_key = value["token"]
        amount_of_cell[actual_key] += 1
        board_copy[position_on_the_board[0]][position_on_the_board[1]] = actual_key

        is_there_winner, winner = ti.three_case_winning(board_copy, amount_to_win)

        if is_there_winner:
            if winner == 'No one':
                total_value += 500
            elif winner == player:
                total_value += 10000000
            else:
                total_value += 10000

    return total_value


def all_option_in_one_turn(board: List[List[str]], amount_to_win: int, players_token: dict, player_key: int) -> list[
    list[list[str]]]:
    # will contain all the information for all the possible board to the depth
    all_boards = []
    winning = False
    if not ti.three_case_winning(board, amount_to_win)[0]:
        all_move = generate_moves(board)

        for e in all_move:
            copy_board = copy.deepcopy(board)
            # play all the moves for this turn
            copy_board[e[0]][e[1]] = players_token[player_key]
            all_boards.append(copy_board)
    return all_boards


def all_options_to_depth(board: List[List[str]], amount_to_win: int, player_token: dict, player_key: int, depth: int) -> list[list[str]]:
    all_game_possible = [board]
    finished_board = []
    board_l = len(board)
    data_path = f"{board_l}x{board_l}"
    data_base = {data_path: {}}

    while depth > 0:
        depth_state = 0
        for i, e in enumerate(all_game_possible):
            data_secondary_path = {f"option {i}": {}}
            for j, k in enumerate(all_option_in_one_turn(e, amount_to_win, player_token, player_key)):
                data_final_path = f"option {j}"
                all_game_possible.append(k)
                dict_info = {
                    "Board": f"{k}",
                    "Depth": f"{depth_state}",
                    "Winning": f"{ti.three_case_winning(k,amount_to_win)}"
                }
                data_secondary_path.setdefault(data_final_path, {}).update(dict_info)
                data_base[data_path].update(data_secondary_path)
            finished_board.append(e)
            all_game_possible.remove(e)

            player_key = player_key + 1
            depth_state = depth_state + 1
            if player_key > len(player_token):
                player_key = 1
        depth = depth - 1
        with open('Tic_data.json','w') as file:
            json.dump(data_base, file, indent=6)
        file.close()
    return all_game_possible





def give_board_new_tile(board, row_emplacement, emplacement_value, type_to_place):
    new_board = deepcopy(board)
    new_board[row_emplacement][emplacement_value] = type_to_place
    return new_board


def generate_moves(game_state) -> list[list[int, int]]:
    """
    Look at a board and everything that is still free is return
    :param game_state: The board of the current game that we need to evaluate
    :return: all the move that we technically could do at a certain point
    """
    legal_move = []
    for e, row in enumerate(game_state):
        for k, cell in enumerate(row):
            if cell == ' ':
                legal_move.append([e, k])
    return legal_move
