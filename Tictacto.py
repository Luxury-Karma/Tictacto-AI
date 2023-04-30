import re

import minMax_AI_Tictac as minMax

def get_integer_input(prompt):
    value = []
    while True:
        user_input = input(prompt)
        user_input = user_input.split()

        if len(user_input) == 2:
            for e in user_input:
                if e.isdigit() or (e.startswith('-') and e[1:].isdigit()):
                    value.append(int(e) - 1)
                else:
                    print('Invalid coordonate')
                    break

            break
        else:
            print('Need to be in the model of 2 numbers like this :  12 5 (first number if the colon second is row)')
    return value


def player_input(board):
    coordonate_good = True
    coordonate = get_integer_input(f'Enter the coordinate from {1} to {len(board)} ex : 1 2')
    while not coordonate_good:
        if 0 > coordonate[1] >= len(board) or coordonate[1] < 0:
            print(f'The row is not correct should be bigger than 0 and smaller {len(board)} you entered {coordonate[1]}\n'
                  f'Enter the coordonate again')
        else:
            coordonate_good = True
            coordonate = get_integer_input(f'Enter the coordinate from {1} to {len(board)} ex : 1 2')
        if 0> coordonate[0] >= len(board) or coordonate[1] < 0:
            print(f'The colon is not correct should be bigger than 0 and smaller {len(board)} you entered {coordonate[1]}\n'
                  f'Enter the coordonate again')
            coordonate = get_integer_input(f'Enter the coordinate from {1} to {len(board)} ex : 1 2')
        else:
            coordonate_good = True
    return coordonate


def give_board_new_tile(board, row_emplacement, emplacement_value, type_to_place):
    board[row_emplacement][emplacement_value] = type_to_place
    return board


import re

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
    for i in range(board_size):
        diag = [board[row][row + i] for row in range(board_size - i)] + \
               [board[row + i][row] for row in range(board_size - i)]
        result, winner = check_line(diag)
        if result:
            return [result, winner]

    # Check diagonal right-to-left
    for i in range(board_size):
        diag = [board[row][board_size - 1 - row - i] for row in range(board_size - i)] + \
               [board[row + i][board_size - 1 - row] for row in range(board_size - i)]
        result, winner = check_line(diag)
        if result:
            return [result, winner]

    # Check if the board is full
    if all(char != ' ' for row in board for char in row):
        return [True, 'No one']

    return [False, '']




def print_board(board):
    index: int = 1
    for e in board:
        if index == 1:
            temp_array = []
            number_of_cell = 1
            for i in range(len(e)):
                temp_array.append(f'{number_of_cell}')
                number_of_cell = number_of_cell + 1
            print(f'{0}: {temp_array}')

        print(f'{index}: {e}')
        index = index + 1


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


def play_against_AI():
    winning = False
    board = board_creation(3)
    token = {1: 'X', 2: 'O'}
    while not winning:
        player = player_turn(board,token[1], 3)
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
    play_against_AI()


    #board = board_creation(5)
    #player_token = ['X', 'O']
    #i = True
    #playing = True
    #number_of_occurence_to_win = 2
    #while playing:
    #    i = not i
    #    p = player_turn(board, player_token[int(i)], number_of_occurence_to_win)
    #    board = p[0]
    #    if p[1][0]:
    #        print(f'{p[1][1]} WIN')
    #        print_board(board)
    #        playing = False
    #        continue


if __name__ == '__main__':
    main()