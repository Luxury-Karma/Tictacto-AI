class AI:
    def __init__(self, board: list[list[str]], my_token: str, ennemi_tokens: list[str]) -> None:
        self.board: list[list[str]] = board
        self.my_token: str = my_token
        self.ennemi_tokens:list[str] = ennemi_tokens
        self.empty_board: list[list[str]] = board
        ...

    def board_update(self, new_board: list[list[str]]) -> None:
        ...

    def split_tables(self) -> list[list[list[str]]]:
        ...

    def copy_empty_board(self) -> list[list[str]]:
        ...