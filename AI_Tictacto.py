class AI:

    def __init__(self, board, my_token, ennemi_tokens):
        self.board = board
        self.my_token = my_token
        self.ennemi_tokens = ennemi_tokens
        self.empty_board = board

    def board_update(self, new_board):
        self.board = new_board

    def copy_empty_board(self):
        return [['' for _ in range(len(self.empty_board[0]))] for _ in range(len(self.empty_board))]

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

