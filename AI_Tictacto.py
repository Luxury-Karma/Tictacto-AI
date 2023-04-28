class AI:

    def __init__(self, board, my_token, ennemi_tokens):
        self.board = board
        self.my_token = my_token
        self.ennemi_tokens = ennemi_tokens
        self.empty_board = board

    def board_update(self, new_board):
        self.board = new_board

    def split_tables(self):
        """
        Split the board to see him self and the other player individually
        :return: a list of individual other player list and its own move
        """
        p_boards = [[]]

        # Split the board
        for e in self.ennemi_tokens:

        return p_boards
