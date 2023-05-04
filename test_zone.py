import json
import statistics
import time
import Tictacto as ti
import minMax_AI_Tictac as minMax
from multiprocessing import Pool, Manager
from functools import partial
import math
from modules.utils import *


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


# TODO: Redo the data base how its built
# TODO : It need to be parallel and making call and not DEEP DIIIIVE
""""
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
"""
def generate_json_data(board: list[list[str]], current_depth: int, max_depth: int, amount_to_win: int, player_token: dict, player_key: int, point_of_board: int, memo: dict = {}, path: str = "") -> dict:
    global moves_done
    global elapse

    board_key, existing_key = check_memo(board, memo)

    if existing_key is not None:
        return {"ref": existing_key}

    key = f"{board_key}"
    data_structure = create_data_structure(key, board, current_depth, amount_to_win, point_of_board,player_token[player_key])

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


def update_progress(moves_done, max_depth, total_possibilities, board):
    r = "\\", "|", "/", "-"
    expected_move_still_needed = total_possibilities - moves_done

    if not elapse:  # Check if elapse is empty
        t = 0
    else:
        t = (statistics.median(elapse) * expected_move_still_needed)

    clear_screen()
    print(f'{r[moves_done % 4]} calculating expected time {str(t)}, expected_move_still_needed{expected_move_still_needed}')
    return moves_done / max_depth



def calculate_board_worth_for_player(players_tokens: dict[int:dict], evaluating_player: int, board: list[list[str]], distance_to_win: int,
                                     empty_cell: str, value_empty: int, value_to_win: int, value_to_block_win: int,
                                     value_towards_win: int, value_towards_blocking_win: int, memo: dict ) -> int:
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


from itertools import repeat

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





def main():
    size = 5
    amount_to_win = 3
    players_token = {1: {'token': 'X', 'amount played': 0}, 'token': 'X', 'amount played': 0}
    player_key = 1
    board = ti.board_creation(size)
    player_actions: list[int] = []
    max_depth = 10
    total_possibilities = count_possibilities(board, 0, max_depth, amount_to_win, players_token, player_key)
    print(f"Total number of possibilities: {total_possibilities}")

    board_worth = calculate_board_worth_for_player(players_token, player_key, board, amount_to_win, ' ', 1, 20, 15, 7, 5)

    # Use a shared memo dictionary to store results of completed tasks
    manager = Manager()
    memo = manager.dict()

    # Partially apply the function to make it suitable for parallel execution
    generate_json_data_with_memo = partial(generate_json_data, memo=memo)

    # Parallelize the execution using a process pool
    with Pool(processes=4) as pool:
        _ = pool.apply(generate_json_data_with_memo, (board, 0, max_depth, amount_to_win, players_token, player_key, board_worth))

    # Now update the progress using the total_possibilities calculated earlier
    progress = update_progress(moves_done, max_depth, total_possibilities, board)

    # Save the memo dictionary to the JSON file
    with open(f'{size}x{size}.json', 'w') as outfile:
        json.dump(dict(memo), outfile, indent=4)

if __name__ == '__main__':
    main()




# surounding evaluation :


import copy

def surrounding_evaluation(surrounding: list[str], players_token: {int, str}, active_player: int, empty_cell: str,
                           value_empty: int, value_to_win: int, value_to_block_win: int, value_towards_win: int,
                           value_towards_blocking_win: int, amount_to_win: int, board: list[list[str]],
                           position_on_the_board: list[int]) -> float:
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
    amount_of_cell: dict = {}
    player = players_token[active_player]['token']
    # Find all the others possible cells
    for key, value in players_token.items():
        amount_of_cell[value["token"]]: int = 0
    for _, value in players_token.items():
        actual_key = value["token"]
        board_copy = copy.deepcopy(board)
        amount_of_cell[actual_key] = amount_of_cell[actual_key] + 1
        board_copy[position_on_the_board[0]][position_on_the_board[1]] = actual_key
        for e in surrounding:
            # give value for the empty cells around
            if e == empty_cell:
                total_value = total_value + value_empty
            # give value for one other cell of its own
            elif e == player:
                total_value = total_value + value_towards_win
                amount_of_cell[actual_key] = amount_of_cell[actual_key] + 1
                if amount_of_cell[actual_key] >= amount_to_win - 1:
                        total_value = total_value + value_to_win
            # give value for anything else
            else:
                total_value = total_value + value_to_block_win
                amount_of_cell[actual_key] = amount_of_cell[actual_key] + 1
                # If another player have more than 2 cell in the zone he might win
                if amount_of_cell[actual_key] >= amount_to_win - 1:
                    total_value = total_value + value_towards_blocking_win
        is_there_winner = ti.three_case_winning(board_copy, amount_to_win)  # evaluation if there is a winner in that world
        if is_there_winner[0] and is_there_winner[1] != '':
            if is_there_winner[1] == 'No one':
                total_value = total_value + 500  # points for an equality
            else:
                if is_there_winner[1] == player:
                    total_value = total_value + 10000000  # amount of point to win
                else:
                    total_value = total_value + 1000000  # amount of point to block a win
    return total_value
