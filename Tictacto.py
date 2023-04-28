import regex


def get_integer_input(prompt) -> [int,int]:
    value: [int, int] = []
    while True:
        user_input = input(prompt)
        user_input = user_input.split()

        if len(user_input) == 2:
            for e in user_input:
                if e.isdigit() or (e.startswith('-') and e[1:].isdigit()):
                    #if int(e)-1 < 0 or int(e)-1>max_size:
                    #    print('out limit')
                    #    break

                    value.append(int(e) - 1)
                else:
                    print('Invalid coordonate')
                    break

            break
        else:
            print('Need to be in the model of 2 numbers like this :  12 5 (first number if the colon second is row)')
    return value


def player_input(board: list[list[str]]) -> [int, int]:
    coordonate_good: bool = False
    coordonate: [int, int] = get_integer_input(f'Enter the coordinate from {1} to {len(board)} ex : 1 2')
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


def give_board_new_tile(board: list[list[str]], row_emplacement: int, emplacement_value: int,
                        type_to_place: str) -> list[list[str]]:
    """
    Will place a specific tile at a specific spot
    :param row_emplacement: the emplacement of the row
    :param board: a list of string
    :param emplacement_value: the emplacement the value will go in the list
    :param type_to_place: the data to put at the emplacement
    :return: the board with the effects
    """
    board[row_emplacement][emplacement_value] = type_to_place
    return board


def three_case_winning(board: list[list[str]], number_of_recurence:int) -> [bool, str]:
    board_l = len(board)
    max_amount = len(board) * len(board)
    b = ''.join([elem for row in board for elem in row])
    dif =''.join([elem for row in board for elem in row if elem and elem != ' '])
    unique_chars = sorted(list(set(dif)))

    for char_player in unique_chars:
        b = b.strip()
        pattern = rf'{char_player}((.{{0}}|.{{{board_l-1,board_l}}}){char_player}){{{number_of_recurence}}}'
        r1 = regex.compile(pattern)  # angle and Vertical
        #pattern = f'{char_player}(.{{{}}}{char_player}){{{number_of_recurence}}}'
        r2 = regex.compile(pattern)  # vertical
        #pattern = f'{char_player}(.{{{0}}}{char_player}){{{number_of_recurence}}}'
        r3 = regex.compile(pattern)  # Check Horizontal
        print(len(b))
        if regex.match(r1,b):
            return [True, char_player]
        if regex.match(r2,b):
            return [True, char_player]
        if regex.match(r3,b):
            return [True, char_player]
    if len(b) == max_amount:
        return [True, 'No one']
    return [False,'']


def print_board(board: list[list[str]]) -> None:
    for e in board:
        print(e)


def player_turn(board: list[list[str]], player_token: str, number_of_occurence_to_win: int) -> list[list[list[str]], list[bool, str]]:
    """
    What happen in a player turn
    :param board:the gaming board
    :param player_token: What the player is represented by
    :return: a list with the board and a list with if anyone win. The bool represent it and the str is who if any
    """
    print_board(board)
    p_inp: list[int, int] = player_input(board)
    board = give_board_new_tile(board, p_inp[0], p_inp[1], player_token)
    # win = winning_condition(board)
    win = three_case_winning(board, number_of_occurence_to_win)
    return [board, win]


def board_creation(size: int) -> list[list[str]]:
    board: list[list[str]] = []
    if size <= 1 or (size % 2) == 0:
        print('the size need to be bigger than 1 and odd\n automated size applied')
        size = size + 1
    for _ in range(size):
        temp_row: list[str] = []
        for _ in range(size):
            temp_row.append(' ')
        board.append(temp_row)
    return board


def main():
    board = board_creation(3)
    player_token: [str] = ['X','O']
    i = True
    playing: bool = True
    number_of_occurence_to_win: int = 2
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



'''
It will look at the board and look value from 0 to 4.
It will choose by the highest value and that's how it will play
if 2 value or more have the exact same value it will play one of them randomly

['0', '0', '0', '0', '0'] | ['2', ' ', '2', ' ', '2'] | [' ', ' ', ' ', 'X', ' '] | [' ', ' ', ' ', ' ', 'X']
['0', '2', '2', '2', '0'] | [' ', '1', '1', '1', ' '] | [' ', ' ', ' ', ' ', ' '] | [' ', 'O', ' ', '4', ' ']
['0', '2', '3', '2', '0'] | ['2', '1', 'X', '1', '2'] | [' ', 'O', '3', 'O', ' '] | [' ', '3', 'X', ' ', ' ']
['0', '2', '2', '2', '0'] | [' ', '1', '1', '1', ' '] | [' ', ' ', ' ', ' ', ' '] | [' ', 'O', ' ', ' ', ' ']
['0', '0', '0', '0', '0'] | ['2', ' ', '2', ' ', '2'] | [' ', ' ', ' ', ' ', ' '] | [' ', ' ', ' ', ' ', ' ']
This is an exemple with a 5 x 5

this is an exemple in a 3 x 3 

['1', '1', '1'] | ['2', '1', '2'] | ['3', '1', '1'] | ['X', '1', 'O'] | ['X', '1', '2'] | ['X', '1', '2']
['1', '3', '1'] | ['1', 'O', '1'] | ['1', 'O', 'X'] | ['4', '1', '3'] | ['1', '1', '1'] | ['1', '0', '1']
['1', '1', '1'] | ['2', '1', '2'] | ['2', '1', 'O'] | ['X', '1', 'O'] | ['2', '1', '2'] | ['2', '0', 'O']
'''
class AI :

    '''
    WILL NEED :
    1) to evaluate the board position with where it would be the most value to be in
    2) to be able to do it with more than 2 players
    3) know who he is and know who the others are
    4) play on any size board

    WILL NEED OPTIMISATION BADLY i want it to play fast fast fast so it don't take years to play a shit load of games
    GOAL : BE able to play a shit load of game and create a file of data to train an AI that is data base and play
            like a pro would
    '''

    def __init__(self, board: list[list[str]], my_token,ennemi_tokens):
        self.board = board
        self.my_token = my_token
        self.ennemi_tokens = ennemi_tokens
        self.empty_board = board

    def board_update(self, new_board: list[list[str]]) -> None:
        self.board = new_board


    def split_tables(self) -> list[list[list[str]]]:
        """
        Split the board to see him self and the other player individualy
        :return: a list of individual other player list and its own move
        """
        p_boards: list[list[list[str]]] = [[[]]]
        #split the board
        for e in self.ennemi_tokens:

        return p_boards

