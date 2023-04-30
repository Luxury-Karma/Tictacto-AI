import Tictacto as ti
from typing import Dict, List, Tuple, Union


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


def evaluation_function(game_state: List[List[str]], player: int, token: str) -> float:
    def count_patterns(pattern: List[str]) -> int:
        count = 0
        for row in game_state:
            count += row.count(pattern)
        for col in range(len(game_state[0])):
            column = [game_state[row][col] for row in range(len(game_state))]
            count += column.count(pattern)
        return count

    def count_diagonal_patterns(pattern: List[str]) -> int:
        count = 0
        diagonals = [game_state[::-1], game_state]

        for diagonal in diagonals:
            for i in range(len(diagonal) - len(pattern) + 1):
                for j in range(len(diagonal[0]) - len(pattern) + 1):
                    if all(diagonal[i + x][j + x] == pattern[x] for x in range(len(pattern))):
                        count += 1
        return count

    three_in_a_row = [token] * 3
    two_in_a_row = [token] * 2 + [" "]

    row_count = count_patterns(three_in_a_row) * 100 + count_patterns(two_in_a_row) * 10
    diagonal_count = count_diagonal_patterns(three_in_a_row) * 100 + count_diagonal_patterns(two_in_a_row) * 10

    score = row_count + diagonal_count
    return score



def maxN(game_state: List[List[str]], depth: int, current_player: int, total_players: int, player_tokens: Dict[int, str]) -> Union[List[float], Tuple[Tuple[int, int], List[float]]]:
    if ti.three_case_winning(game_state, 3)[0] or depth == 0:
        return [evaluation_function(game_state, player, player_tokens[player]) for player in range(1, total_players + 1)]

    max_scores = [float('-inf')] * total_players
    best_move = None

    for move in generate_moves(game_state):
        new_game_state = ti.give_board_new_tile(game_state, move[0], move[1], player_tokens[current_player])
        next_player = current_player % total_players + 1
        scores = maxN(new_game_state, depth - 1, next_player, total_players, player_tokens)

        if scores[current_player - 1] > max_scores[current_player - 1]:
            max_scores = scores
            best_move = move

    return max_scores if depth > 1 else (best_move, max_scores)


def ai_move(game_state: List[List[str]], current_player: int, total_players: int, player_tokens: Dict[int, str], depth_limit:int) -> Tuple[int, int]:
    best_move, _ = maxN(game_state, depth_limit, current_player, total_players, player_tokens)
    return best_move


# Game state to see what it does
Test_game_state = [[' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', 'O', ' '],
                   [' ', ' ', 'O', 'X', ' '],
                   [' ', ' ', ' ', ' ', 'O'],
                   ['X', ' ', ' ', 'X', ' ']]

board = ti.board_creation(5)


players = {1: 'X', 2: 'O'}
players_num = len(players)
future_sight = 5
ai_move(board, 1, players_num, players, future_sight)
#while not ti.three_case_winning(board,3)[0]:
#    first_player = ai_move(board, 1, players_num, players, future_sight)
#    board = ti.give_board_new_tile(first_player[0], first_player[1])
#    second_player = ai_move(board, 1,players_num, players, future_sight)



