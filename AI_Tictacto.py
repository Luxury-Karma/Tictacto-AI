class AI:
    '''
    It will look at the board and look value from 0 to 4. It will choose by the highest value and that's how it will play
    if 2 value or more have the exact same value it will play one of them randomly

    ['0', '0', '0', '0', '0'] | ['2', ' ', '2', ' ', '2'] | [' ', ' ', ' ', 'X', ' '] | [' ', ' ', ' ', ' ', 'X']
    ['0', '2', '2', '2', '0'] | [' ', '1', '1', '1', ' '] | [' ', ' ', ' ', ' ', ' '] | [' ', 'O', ' ', '4', ' ']
    ['0', '2', '3', '2', '0'] | ['2', '1', 'X', '1', '2'] | [' ', 'O', '3', 'O', ' '] | [' ', '3', 'X', ' ', ' ']
    ['0', '2', '2', '2', '0'] | [' ', '1', '1', '1', ' '] | [' ', ' ', ' ', ' ', ' '] | [' ', 'O', ' ', ' ', ' ']
    ['0', '0', '0', '0', '0'] | ['2', ' ', '2', ' ', '2'] | [' ', ' ', ' ', ' ', ' '] | [' ', ' ', ' ', ' ', ' ']
    This is an exemple with a 5 x 5

    this is an exemple in a
    3x3

    ['1', '1', '1'] | ['2', '1', '2'] | ['3', '1', '1'] | ['X', '1', 'O'] | ['X', '1', '2'] | ['X', '1', '2']
    ['1', '3', '1'] | ['1', 'O', '1'] | ['1', 'O', 'X'] | ['4', '1', '3'] | ['1', '1', '1'] | ['1', '0', '1']
    ['1', '1', '1'] | ['2', '1', '2'] | ['2', '1', 'O'] | ['X', '1', 'O'] | ['2', '1', '2'] | ['2', '0', 'O']
    '''

    def __init__(self, board, my_token, ennemi_tokens, how_many_token_to_win):
        self.board = board
        self.my_token = my_token
        self.ennemi_tokens = ennemi_tokens
        self.empty_board = board
        self.how_many_to_win: int = how_many_token_to_win

    def board_update(self, new_board):
        self.board = new_board

    def copy_empty_board(self):
        return [[' ' for _ in range(len(self.empty_board[0]))] for _ in range(len(self.empty_board))]

    def copy_empty_board_integer(self):
        return [[0 for _ in range(len(self.empty_board[0]))] for _ in range(len(self.empty_board))]

    def split_tables(self):
        """
        Split the board to see him self and the other player individually
        :return: a list of individual other player list and its own move
        """
        p_boards = []

        # Split the board
        for e in self.ennemi_tokens:
            temp_board = self.copy_empty_board()

            for i, row in enumerate(self.board):
                for j, cell in enumerate(row):
                    if cell == e or cell == self.my_token:
                        temp_board[i][j] = cell

            p_boards.append([temp_board])

        print(p_boards)
        return p_boards

    def check_emplacement_arround_cell(self, cell_emplacement):
        """
        :param cell_emplacement: where we want to look
        :return: list of integer that represent the emplacement top, down, left, right
        """
        row, col = cell_emplacement
        return [(-row), (+len(self.board)) - -(row - 1), (-col), (+len(self.board[0]) - col - 1)]


    # Try to make a basic around point so if you are X away have a + 2 or + 1 or - 1 or + 0 (ignore)
    # THIS ONE ONLY ACT KNOWING THE ENNEMIE

    def check_board_for_point(self,cell_emplacement:list[int], looking_board: list[list[int]]) :
        max_emplacement = self.check_emplacement_arround_cell(self, cell_emplacement)
        for e,position in enumerate(max_emplacement):
            point_given: int = 1
            if abs(e) <= self.how_many_to_win:
                if position == 1 or position == 2:
                    # look as much top as possible and closer we are of the limit to win we give more point of +1
                    for k in range(e):
                        looking_board[e][cell_emplacement[1]] = looking_board[e][cell_emplacement[1]] + point_given











    def options_evaluation_process(self, individual_board):
        """
        will look at the board remove all the allready played move and calculate wich option give
        the most chance of winning
        :return: an list of list of integer showing wich one is the best
        """
        Unplayable_cells: list[list[int]] = []
        own_cells: list[[int]] = []
        # Playing with the string board to look what is happening
        for e, row in enumerate(self.board):
            for i, cell in enumerate(row):
                if cell != ' ':
                    if cell == self.my_token:
                        own_cells.append([[e, i]])
                    else:
                        Unplayable_cells.append([e, i])
        # applying what we saw mathematically
        all_integer_boards: list[list[list[int]]] = []
        for e in individual_board:
            integer_board: list[[int]] = self.copy_empty_board_integer()
            for i,row in enumerate(e):
                for j, cell in enumerate(row):
                    # remove the possibility of taking all ready taken case on that board
                    if cell != ' ':
                        # If the cell is own by the ennemie
                        if [i, j] in Unplayable_cells :
                            integer_board[i][j] = integer_board[i][j] - 100

                        # if the cell is own by my self
                        if [i, j] in own_cells:
                            integer_board[i][j] = integer_board[i][j] - 100


            all_integer_boards.append([integer_board])
