class AI:
    def __init__(self, board: list[list[str]], my_token: str, ennemi_tokens: list[str],how_many_token_to_win:int) -> None:
        self.board: list[list[str]] = board
        self.my_token: str = my_token
        self.ennemi_tokens:list[str] = ennemi_tokens
        self.empty_board: list[list[str]] = board
        self.how_many_to_win: int = how_many_token_to_win
        ...

    def board_update(self, new_board: list[list[str]]) -> None:
        ...

    def split_tables(self) -> list[list[list[str]]]:
        ...

    def copy_empty_board(self) -> list[list[str]]:
        ...

    def copy_empty_board_integer(self) -> list[list[int]]:
        ...

    def check_emplacement_arround_cell(self, cell_emplacement: list[int]) -> list[int]:
        ...


    def options_evaluation_process(self, individual_board: list[list[list[str]]]) -> list[list[int]]:
        ...