import copy

import Tictacto as ti
from typing import Dict, List, Tuple, Optional
from copy import deepcopy


def get_directional_neighbors(matrix: List[List[str]], row: int, col: int, distance: int = 1) -> list[str]:
    """
    Look arround a specific cell than return the diagonals, horizontal and vertical cells values
    :param matrix: The array where is the cell you need to look
    :param row: Y axis of the emplacement of the Cell
    :param col: X Axis of the emplacement of the Cell
    :param distance: how much around you need to see
    :return: all the value of the cells around
    """
    neighbors = []
    row_start = max(row - distance, 0)
    row_end = min(row + distance + 1, len(matrix))
    col_start = max(col - distance, 0)
    col_end = min(col + distance + 1, len(matrix[0]))

    for i in range(row_start, row_end):
        for j in range(col_start, col_end):
            if (i == row and j != col) or (i != row and j == col) or (i != row and j != col and abs(i - row) == abs(j - col)):
                neighbors.append(matrix[i][j])

    return neighbors


def surrounding_evaluation(surrounding: list[str],players_token: {int,str}, active_player: int,empty_cell: str,
                           value_empty: int, value_to_win: int, value_to_block_win: int, value_towards_win: int,
                           value_towards_blocking_win: int, amount_to_win: int, board: list[List[str]],
                           position_on_the_board:List[int]) -> float:
    """
    Evaluate the worth of a cell by the surrounding for itself and the other
    :param empty_cell: What a empty cell should look like
    :param surrounding: all the surrounding of one cell
    :param players_token: Who is in the game
    :param active_player: Who am I evaluating for
    :param value_empty: How much an empty cell worth
    :param value_to_win: How much a Winning worth
    :param value_to_block_win: How much blocking a win worth
    :param value_towards_win: How much a cell that give a potential win worth
    :param value_towards_blocking_win: how much blocking a potential win worth
    :return: the value of the specific cell
    """
    total_value: float = 0
    amount_of_my_cell: int = 0
    amount_of_ennemies_cell: dict = {}
    player = players_token[active_player]
    # Find all the others possible cells
    for key, value in players_token.items():
        if key != active_player:
            amount_of_ennemies_cell[value] = 0

    for e in surrounding:
        board_copy = copy.deepcopy(board)
        for _, value in players_token.items():
            if value != player:
                board_copy[position_on_the_board[0]][position_on_the_board[1]] = value
                if ti.three_case_winning(board_copy, amount_to_win)[0]:
                    total_value = total_value + 5000
            elif value == player:
                board_copy[position_on_the_board[0]][position_on_the_board[1]] = value
                if ti.three_case_winning(board_copy, amount_to_win)[0]:
                    total_value = total_value + 10000000

        # give value for the empty cells around
        if e == empty_cell:
            total_value = total_value + value_empty
        # give value for one other cell of its own
        elif e == player:
            total_value = total_value + value_towards_win
            amount_of_my_cell = amount_of_my_cell + 1
            if amount_of_my_cell >= amount_to_win-1:
                total_value = total_value + value_to_win
        # give value for anything else
        else:
            total_value = total_value + value_to_block_win
            amount_of_ennemies_cell[e] = amount_of_ennemies_cell[e] + 1
            # If another player have more than 2 cell in the zone he might win
            if amount_of_ennemies_cell[e] >= amount_to_win-1:
                total_value = total_value + value_towards_blocking_win
    return total_value





def minMax(board: List[List[str]],depth: int, amount_to_win: int, players_token: dict, player_key: int) -> List[List[str]]:
    if not ti.three_case_winning(board, amount_to_win)[0] and depth>0:
        all_move = generate_moves(board)
        copy_board = copy.deepcopy()
        for e in all_move:
            copy_board[e[0]][e[1]] = players_token[player_key]





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











