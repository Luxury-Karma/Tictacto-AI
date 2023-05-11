import math
import statistics
import Tictacto as ti
import minMax_AI_Tictac as minMax
from modules.utils import *
import copy
import json
from json.decoder import JSONDecodeError
from collections import deque
import multiprocessing
import sys
import time


moves_done = 0
elapse = []


def are_boards_mirrored(board1, board2):
    size = len(board1)
    return all(board1[i][j] == board2[j][i] for i in range(size) for j in range(size))


def get_key(board):
    return ''.join([''.join(row) for row in board])


def create_data_structure(key:str, board:list[list[str]], depth: int, amount_to_win: int, point_of_the_board:int, player_token: str, MotherID:str):
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
            "Mother ID": MotherID
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



def update_progress(moves_done, max_depth, total_possibilities, start_time):

    r = "\\", "|", "/", "-"
    expected_move_still_needed = total_possibilities - moves_done

    if moves_done == 0:  # Check if moves_done is 0
        t = 0
    else:
        elapsed_time = time.time() - start_time
        t = elapsed_time * expected_move_still_needed / moves_done

    progress = moves_done / max_depth
    bar_length = 50
    filled_length = int(round(bar_length * progress))

    bar = "=" * filled_length + "-" * (bar_length - filled_length)
    sys.stdout.write(f"\r{r[moves_done % 4]} [{bar}] {progress * 100:.2f}% (Estimated time remaining: {t:.2f}s)")
    sys.stdout.flush()

    return progress



def game_possibilities(board_size: int, max_depth: int, num_players: int) -> int:
    total_cells = board_size * board_size
    possibilities = math.factorial(total_cells) / (math.factorial(total_cells - max_depth) * (num_players ** max_depth))
    return int(possibilities)



# ---------------------------- OPTIMISATION ZONE ------------------------------------------------


# --------------------------------------------------------------------------------------------


# -------------------------------- OPTIMISE TO REPLACE ZONE ----------------------------------

board_worth_cache = {}

def calculate_board_worth(board: list[list[str]], amount_to_win: int, player_token: dict, player_key: int) -> int:
    board_tuple = board_to_tuple(board)
    if board_tuple in board_worth_cache:
        return board_worth_cache[board_tuple]

    total_board_worth: int = 0
    for e, row in enumerate(board):
        for k, cell in enumerate(row):
            total_board_worth += minMax.surrounding_evaluation(
                minMax.get_directional_neighbors(board, e, k, amount_to_win), player_token, player_key, ' ',
                1, 20, 15, 7, 4, amount_to_win, board, [e, k])  # Calculate the worth of a specific board
    board_worth_cache[board_tuple] = total_board_worth
    return total_board_worth




def board_to_tuple(board):
    return tuple(tuple(row) for row in board)


def generate_json_data(board: list[list[str]], depth: int, amount_to_win: int, player_token: dict, player_key: int,
                       id: int) -> None:
    global moves_done
    global elapse
    board_data = deque([(board, None)])  # Add the Mother ID as the second element of the tuple
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
            depth_board, mother_id = board_data.popleft()  # Unpack the tuple to get the board and its Mother ID
            all_possible_move = minMax.generate_moves(depth_board)

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

                json_data = create_data_structure(f'{id:0X}{actual_depth:0X}', board_copy, actual_depth, amount_to_win, board_worth, player_token[player_key]["token"], mother_id) # Format the data

                # Combine the existing data with the new data
                key = list(json_data.keys())[0]  # Get the key of the current data dictionary
                existing_data[key] = json_data[key]  # Add the current data to the existing data using the key

                if not json_data[f'{id:0X}{actual_depth:0X}']["Winning"]:
                    board_data.append((board_copy, key))  # Add the current key as the Mother ID

                # Mark the board as processed
                processed_boards.add(board_tuple)

                id += 1

        actual_depth += 1
        id = 0
        player_key += 1
        if player_key > len(player_token):
            player_key = 1
        depth -= 1

    # Save the updated data back to the file
    with open(filename, 'w') as outfile:
        json.dump(existing_data, outfile, indent=4)
    print(f'Saving we are at depth : {actual_depth}')

#--------------------------------------------------------------------------------------------


def main():
    size = 5
    amount_to_win = 5
    players_token = {1: {'token': 'X', 'amount played': 0}, 2: {'token': 'O', 'amount played': 0}}
    player_key = 1
    board = ti.board_creation(size)
    max_depth = 5
    first_id = 0

    # Calculate gross possibilities of the board
    total_possibilities = game_possibilities(size, max_depth, len(players_token))
    print(total_possibilities)

    # Use multiprocessing to parallelize the code
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    # Call the generate_json_data function for each process in parallel
    start_time = time.time()
    results = [pool.apply_async(generate_json_data,
                                args=(board, max_depth, amount_to_win, players_token, player_key, first_id)) for _ in
               range(num_processes)]

    # Update progress bar
    #while not all(result.ready() for result in results):
    #    moves_done = sum(result._number_left for result in results)
    #    update_progress(moves_done, max_depth, total_possibilities, start_time)
    #    time.sleep(0.5)

    pool.close()
    pool.join()

    update_progress(max_depth, max_depth, total_possibilities, start_time)
    print("\nCompleted.")



if __name__ == '__main__':
    main()


