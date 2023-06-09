import re

import os

import minMax_AI_Tictac as minMax

import test_zone

from modules.utils import *


def give_board_new_tile(board, row_emplacement, emplacement_value, type_to_place):
    board[row_emplacement][emplacement_value] = type_to_place
    return board


def three_case_winning(board, number_of_recurence):
    board_size = len(board)

    def check_line(line):
        count = 0
        prev_char = None
        for char in line:
            if char != ' ' and char == prev_char:
                count += 1
                if count == number_of_recurence:
                    return True, char
            else:
                count = 1
                prev_char = char
        return False, ''

    # Check horizontal
    for row in board:
        result, winner = check_line(row)
        if result:
            return [result, winner]

    # Check vertical
    for col in range(board_size):
        result, winner = check_line([board[row][col] for row in range(board_size)])
        if result:
            return [result, winner]

    # Check diagonal left-to-right
    for i in range(board_size * 2 - 1):
        diag = [board[row][i - row] for row in range(max(i - board_size + 1, 0), min(i + 1, board_size))]
        result, winner = check_line(diag)
        if result:
            return [result, winner]

    # Check diagonal right-to-left
    for i in range(board_size * 2 - 1):
        diag = [board[row][board_size - 1 - (i - row)] for row in range(max(i - board_size + 1, 0), min(i + 1, board_size))]
        result, winner = check_line(diag)
        if result:
            return [result, winner]

    # Check if the board is full
    if all(char != ' ' for row in board for char in row):
        return [True, 'No one']

    return [False, '']


def player_turn(board, player_token, number_of_occurence_to_win):
    print_board(board)
    p_inp = player_input(board)
    board = give_board_new_tile(board, p_inp[0], p_inp[1], player_token)
    win = three_case_winning(board, number_of_occurence_to_win)
    return [board, win]


def board_creation(size):
    board = []
    if size <= 1 or (size % 2) == 0:
        print('the size need to be bigger than 1 and odd\n automated size applied')
        size = size + 1
    for _ in range(size):
        temp_row = []
        for _ in range(size):
            temp_row.append(' ')
        board.append(temp_row)
    return board





# ----------------------------- TESTING AI --------------------------

def Test_AI():
    # Game state to see what it does
    Test_game_state = [[' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', 'O', ' ', ' '],
                       [' ', 'X', 'X', 'O', ' '],
                       [' ', ' ', ' ', ' ', ' '],
                       [' ', ' ', ' ', ' ', ' ']]
    #Test_game_state = board_creation(5)
    #value_array = board_creation(5)
    player_tokens = {1: 'X', 2: 'O'}
    player_playing = 1
    winning = three_case_winning(Test_game_state,3)
    while not winning[0]:
        highest_value = 0
        emplacement = [0, 0]
        for e,row in enumerate(Test_game_state):
            for k,cell in enumerate(row):
                neighbors_cells = minMax.get_directional_neighbors(Test_game_state, e, k, 2)
                new_tile = minMax.surrounding_evaluation(neighbors_cells,player_tokens,player_playing,' ', 1, 20, 10, 8, 3, 3,
                                                         Test_game_state,[e, k])
                if new_tile > highest_value and Test_game_state[e][k] == ' ':
                    highest_value = new_tile
                    emplacement = [e, k]
        give_board_new_tile(Test_game_state, emplacement[0], emplacement[1], player_tokens[player_playing])

        winning = three_case_winning(Test_game_state, 3)
        if winning[0]:
            print_board(Test_game_state)
            print(f'The player {winning[1]} win')
            continue
        else:
            print_board(Test_game_state)
        input('Play next Turn press enter')
        player_playing = player_playing + 1
        if player_playing > len(player_tokens):
            player_playing = 1


def play_against_AI(board_size: int, winning_condition: int):
    winning = False
    board = board_creation(board_size)
    token = {1: 'X', 2: 'O'}
    while not winning:
        player = player_turn(board,token[1], winning_condition)
        board = player[0]
        winning = player[1][0]
        if winning:
            print('Player Win')
            print_board(board)
            continue
        ai_player = AI_playing(board,token,2)
        board = ai_player[0]
        winning = ai_player[1]
        if winning:
            print_board(board)
            print('AI Win')
            continue



def Ai_vs_Ai(board_size: int, winning_condition: int):
    winning = False
    board = board_creation(board_size)
    token = {1: 'X', 2: 'O'}
    index = 1
    while not winning:
        ai_player = AI_playing(board, token, index)
        board = ai_player[0]
        winning = ai_player[1]
        if winning:
            print_board(board)
            print(f'AI {three_case_winning(board,3)[1]} Win')
            continue
        index = index + 1
        if index>len(token):
            index = 1


def AI_playing(board: list[list[str]],token: dict[int:str], AI_token: int):
    highest_value = 0
    emplacement = [0, 0]
    for e, row in enumerate(board):
        for k, cell in enumerate(row):
            neighbors_cells = minMax.get_directional_neighbors(board, e, k, 2)
            new_tile = minMax.surrounding_evaluation(neighbors_cells, token, 2, ' ', 1, 20, 10, 8,
                                                     3, 3,
                                                     board, [e, k])
            if new_tile > highest_value and board[e][k] == ' ':
                highest_value = new_tile
                emplacement = [e, k]
    print(f'AI decided that best move is : {emplacement[0] +1}, {emplacement[1] +1} with the score of : {highest_value}')
    give_board_new_tile(board, emplacement[0], emplacement[1], token[AI_token])
    winning = three_case_winning(board, 3)
    return [board, winning[0]]

#
# ---------------------------------------------------------------

def main():
    #play_against_AI(11, 8)
    player_token = {1: 'X', 2: 'O'}
    test_board = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]
    test_zone.save_json(test_zone.generate_json_data(test_board, 3, 3))
    #print(three_case_winning(test_board, 3))
    #Ai_vs_Ai(3, 3)
    # mimi = minMax.all_options_to_depth(test_board, 3, player_token, 1, 2)
    # save_file('.\\tictacto.txt', mimi)
    # for e in mimi:
    #     print_board(e)

if __name__ == '__main__':
    main()