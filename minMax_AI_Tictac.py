import copy

import Tictacto as ti
from typing import Dict, List, Tuple, Union, Optional
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
    Evaluate the worth of a cell by the surrounding
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

        if e == empty_cell:
            total_value = total_value + value_empty
            board_copy = copy.deepcopy(board)

            board_copy[position_on_the_board[0]][position_on_the_board[1]] = player
            if ti.three_case_winning(board_copy, amount_to_win)[0]:
                total_value = total_value + 10000000
                return total_value
        elif e == player:
            total_value = total_value + value_towards_win
            amount_of_my_cell = amount_of_my_cell + 1
            if amount_of_my_cell >= amount_to_win-1:
                total_value = total_value + value_to_win
        else:
            total_value = total_value + value_to_block_win
            amount_of_ennemies_cell[e] = amount_of_ennemies_cell[e] + 1
            # If an other player have more than 2 cell in the zone he might win
            if amount_of_ennemies_cell[e] >= amount_to_win-1:
                total_value = total_value + value_towards_blocking_win
    return total_value

#def evaluation_function(game_state: List[List[str]], player: int, all_players_token: {}, winning_distance: int) -> float:

    # Value of empty Cell : +1
    # Value that make win the game : +20
    # Value that Block the other to win game: +19
    # Value that make you go to win game : +5
    # Value that block the other to go to make a win: +4
    my_token = all_players_token[player]
    max_value: float = float('-inf')
    looking_length = winning_distance - 1
    for e, row in enumerate(game_state):
        for k, cell in enumerate(row):
            cell_value = 0
            around_value = get_directional_neighbors(game_state, e, k, looking_length)
            # if the cell we meet is not my token then if it can win i Need to block it except if I can win now
            if cell != my_token:
                pass
            # if the cell we meet is my cell i need to look my way to win and if I can
            elif cell == my_token:
                pass
            # if the cell we meet is empty Evaluate value for the amount of space around it have
            elif cell == ' ':
                pass
            # If the cell we look have more value than anyone before change the value of the best value
            if max_value < cell_value:
                max_value = cell_value

    # return the most value cell
    return max_value





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




def maxN(game_state: List[List[str]], depth: int, current_player: int, total_players: int, player_tokens: Dict[int, str]) -> Tuple[Optional[Tuple[int, int]], List[float]]:
    if ti.three_case_winning(game_state, 3)[0] or depth == 0:
        pass
        #return None, [evaluation_function(game_state, player, player_tokens[player]) for player in range(1, total_players + 1)]

    max_scores = [float('-inf')] * total_players
    best_move = None

    for move in generate_moves(game_state):
        new_game_state = give_board_new_tile(game_state, move[0], move[1], player_tokens[current_player])
        next_player = current_player % total_players + 1
        _, scores = maxN(new_game_state, depth - 1, next_player, total_players, player_tokens)

        if scores[current_player - 1] > max_scores[current_player - 1]:
            max_scores = scores
            best_move = move

    return best_move, max_scores




def ai_move(game_state: List[List[str]], current_player: int, total_players: int, player_tokens: Dict[int, str], depth_limit:int) -> Tuple[int, int]:
    best_move, _ = maxN(game_state, depth_limit, current_player, total_players, player_tokens)
    return best_move









