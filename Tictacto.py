import re
import AI_Tictacto as AI
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


def three_case_winning(board, number_of_recurence):
    board_l = len(board)
    max_amount = len(board) * len(board)
    b = ''.join([elem for row in board for elem in row])
    dif = ''.join([elem for row in board for elem in row if elem and elem != ' '])
    unique_chars = sorted(list(set(dif)))
    for char_player in unique_chars:
        b = b.strip()

        pattern = f'{char_player}(.{{{board_l}}}{char_player}){{{number_of_recurence - 1}}}'
        r1 = re.compile(pattern)  # angle left to right
        pattern = f'{char_player}(.{{{board_l-1}}}{char_player}){{{number_of_recurence-1}}}'
        r2 = re.compile(pattern)  # vertical
        pattern = f'{char_player}(.{{{0}}}{char_player}){{{number_of_recurence-1}}}'
        r3 = re.compile(pattern)  # Check Horizontal

        if re.match(r1, b):
            return [True, char_player]
        if re.match(r2, b):
            return [True, char_player]
        if re.match(r3, b):
            return [True, char_player]

    if len(b) == max_amount and unique_chars != []:
        return [True, 'No one']
    return [False, '']


def print_board(board):
    for e in board:
        print(e)


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
                       [' ', ' ', ' ', 'O', ' '],
                       [' ', ' ', 'O', 'X', ' '],
                       [' ', ' ', ' ', ' ', 'O'],
                       ['X', ' ', ' ', 'X', ' ']]
    Test_game_state = board_creation(21)
    value_array = board_creation(21)
    player_tokens = {1: 'X', 2: 'O'}
    while True:
        for e, row in enumerate(Test_game_state):
            for k, cell in enumerate(row):
                neighbors = minMax.get_directional_neighbors(Test_game_state, e, k, 2)
                player = 1
                # array for X
                value_array[e][k] = minMax.surrounding_evaluation(neighbors, player_tokens, player, ' ', 1, 20, 15, 5, 4, 3)

        print('BOARD FOR X :')
        best_value_array = [[0,0], 0]
        for e, row in enumerate(value_array):
            for k,cell in enumerate(row):
                if cell > best_value_array[1] and Test_game_state[e][k] == ' ':
                    best_value_array[0] = [e, k]
                    best_value_array[1] = cell
        row = best_value_array[0][0]
        col = best_value_array[0][1]
        Test_game_state[row][col] = player_tokens[1]
        winning = three_case_winning(Test_game_state,3)
        if winning[0]:
            print_board(Test_game_state)
            print(f'{winning[1]} Win')
            break
        print(f'The best cell is : {best_value_array[0]} with {best_value_array[1]} points')



        print('---------')
        for e, row in enumerate(Test_game_state):
            for k, cell in enumerate(row):
                neighbors = minMax.get_directional_neighbors(Test_game_state, e, k, 2)
                player = 2
                # array for O
                value_array[e][k] = minMax.surrounding_evaluation(neighbors, player_tokens, player, ' ', 1, 20, 19, 5, 4, 3)
        winning = three_case_winning(Test_game_state, 3)
        if winning[0]:
            print_board(Test_game_state)
            print(f'{winning[1]} Win')
            break
        for e, row in enumerate(value_array):
            for k,cell in enumerate(row):
                if cell > best_value_array[1] and Test_game_state[e][k] == ' ':
                    best_value_array[0] = [e, k]
                    best_value_array[1] = cell
        print(f'The best cell is : {best_value_array[0]} with {best_value_array[1]} points')
        print('---------')
        row = best_value_array[0][0]
        col = best_value_array[0][1]
        Test_game_state[row][col] = player_tokens[2]



#
# ---------------------------------------------------------------

def main():
    #Test_AI()
    test = [['X', ' ', ' '],
            [' ', 'X', 'X'],
            [' ', ' ', ' ']]
    test_two = [[' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', 'X'],
                [' ', ' ', ' ', 'X', ' '],
                [' ', ' ', 'X', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ']]
    test_three =[[' ', ' ', ' ', ' ', ' '],
                [' ', ' ', 'X', ' ', ' '],
                [' ', ' ', ' ', 'X', ' '],
                [' ', ' ', ' ', ' ', 'X'],
                [' ', ' ', ' ', ' ', ' ']]
    test = [['X', ' ', 'X'],
            [' ', 'X', ' '],
            [' ', ' ', ' ']]
    test_for = [[' ', ' ', 'X'],
                [' ', 'X', ' '],
                ['X', ' ', ' ']]
    print(three_case_winning(test,3)[0])
    print(three_case_winning(test_two,3)[0])
    print(three_case_winning(test_three,3)[0])
    print(three_case_winning(test_for,3)[0])

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