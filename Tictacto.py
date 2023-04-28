import re
import AI_Tictacto as AI

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
    coordonate_good = False
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
        pattern = rf'{char_player}((.{{0}}|.{{{board_l-1,board_l}}}){char_player}){{{number_of_recurence}}}'
        r1 = re.compile(pattern)
        r2 = re.compile(pattern)
        r3 = re.compile(pattern)
        print(len(b))
        if re.match(r1, b):
            return [True, char_player]
        if re.match(r2, b):
            return [True, char_player]
        if re.match(r3, b):
            return [True, char_player]
    if len(b) == max_amount:
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

def test_ai():
    board = [[' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ']]
    full_board = [['X', 'X', 'Z', ' ', 'Z'],
                  [' ', 'O', ' ', ' ', ' '],
                  [' ', ' ', 'K', ' ', ' '],
                  [' ', ' ', ' ', 'O', ' '],
                  [' ', ' ', 'K', ' ', ' ']]

    ai = AI.AI(board, 'X', ['O', 'Z', 'K'])
    ai.board_update(full_board)
    split_table = ai.split_tables()

# ---------------------------------------------------------------

def main():
    test_ai()

    board = board_creation(5)
    player_token = ['X', 'O']
    i = True
    playing = True
    number_of_occurence_to_win = 2
    while playing:
        i = not i
        p = player_turn(board, player_token[int(i)], number_of_occurence_to_win)
        board = p[0]
        if p[1][0]:
            print(f'{p[1][1]} WIN')
            print_board(board)
            playing = False
            continue


if __name__ == '__main__':
    main()