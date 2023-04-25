import math


def get_integer_input(prompt) -> int:
    while True:
        user_input = input(prompt)
        if user_input.isdigit() or (user_input.startswith('-') and user_input[1:].isdigit()):
            value = int(user_input)
            break
        else:
            print("Please enter a valid integer.")
    return value


def player_input(board: list[list[str]]) -> [int, int]:
    row_is_fine: bool = False
    emplacement_is_fine: bool = False
    row: int = -1
    emplacement: int = -1
    while not row_is_fine:
        row = get_integer_input(f'Wich row will you take you have from 1 to {len(board)}')
        if row <= len(board):
            empty = False
            for e in board[row-1]:
                if e == '':
                    empty = True
                    break
            if empty:
                row_is_fine = True
            continue
        print(f'The row need to be in between 0 and {len(board)}')
    while not emplacement_is_fine:
        emplacement = get_integer_input(f'wich emplacement you will take from 1 to {len(board[1])}')
        if emplacement <= len(board[1]):
            if board[row-1][emplacement-1] == '':
                emplacement_is_fine = True
                continue
            print('The value might have been use')
        print(f'The emplacement need to be in between one and {len(board[1])}')
    return [row-1, emplacement-1]


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


def winning_condition(board: list[list[str]]) -> [bool, str]:
    """
    receive a board of any size as long as they are odd and give if there is a legal tictacto win
    :param board: a 2D list of list of string
    :return: if there is a victory and the player that win if any return false and '' if none
    """
    win: bool = False
    winner: str = ''
    # Horizontal Win
    for e in board:
        value_check: str = e[0]  # Take the first value
        if value_check != '':  # Ensure the value is not empty
            win = True
            for k in e:
                if k != value_check:
                    win = False
                    break
            if win:
                return [win, value_check]  # Horizontal Win

    # Vertical win
    value_check = ''
    for e in range(len(board[0])):
        for k in range(len(board)):
            # give the looking value
            if k == 0:
                win = True
                value_check = board[k][e]
                # mean that we can't win that way
                if value_check == '':
                    win = False
                    break
            # look if we can't win
            if board[k][e] != value_check:
                win = False
                break
        if win:
            return [win, value_check]

    # Check for angles win
    # calculate the center of the board
    row_center: int = math.ceil(len(board)/2)-1
    emplacement_center: int = math.ceil(len(board[0])/2)-1
    if board[row_center][emplacement_center] != '':
        value_check = board[row_center][emplacement_center]
        i: int = row_center
        y: int = emplacement_center
        # Check for a left Angle
        win = True
        # top left
        while i >= 0 and y >= 0 and win:
            if board[i][y] != value_check:
                win = False
                break
            i = i-1
            y = y-1
        i = row_center
        y = emplacement_center
        # down right
        while i < len(board) and y < len(board[0]) and win:
            if board[i][y] != value_check:
                win = False
                break
            i = i+1
            y = y+1
        if win:
            return [win, value_check]
        i = row_center
        y = emplacement_center
        # Check for a right Angle
        win = True
        # top right
        while i >= 0 and y <= len(board[0]) and win:
            if board[i][y] != value_check:
                win = False
                break
            i = i - 1
            y = y + 1
        i = row_center
        y = emplacement_center
        # down left
        while i <= len(board) and y >= 0 and win:
            if board[i][y] != value_check:
                win = False
                break
            i = i + 1
            y = y - 1
        if win:
            return [win, value_check]
    return [win, winner]


def print_board(board: list[list[str]]) -> None:
    for e in board:
        print(e)


def player_turn(board: list[list[str]], player_token: str) -> list[list[list[str]], list[bool, str]]:
    """
    What happen in a player turn
    :param board:the gaming board
    :param player_token: What the player is represented by
    :return: a list with the board and a list with if anyone win. The bool represent it and the str is who if any
    """
    print_board(board)
    p_inp: list[int, int] = player_input(board)
    board = give_board_new_tile(board, p_inp[0], p_inp[1], player_token)
    win = winning_condition(board)
    return [board, win]


def board_creation(size: int) -> list[list[str]]:
    board: list[list[str]] = []
    if size <= 1 or (size%2)==0:
        print('the size need to be bigger than 1 and odd\n automated size applied')
        size = 3
    for i in range(size):
        temp_row: list[str] = []
        for k in range(size):
            temp_row.append('')
        board.append(temp_row)
    return board

def main():
    board = board_creation(3)
    print_board(board)
    print('------------------')
    player_token: [str] = ['X', 'O']
    i = 0
    playing: bool = True
    while playing:
        p = player_turn(board, player_token[i])
        board = p[0]
        if p[1][0]:
            print(f'{p[1][1]} WIN')
            playing = False
            continue
        i = i + 1
        if i > len(player_token)-1:
            i = 0


if __name__ == '__main__':
    main()
