

def get_integer_input(prompt: str) -> tuple[int, int]:
    ...

def player_input(board: list[list[str]]) -> tuple[int, int]:
    ...

def give_board_new_tile(board: list[list[str]], row_emplacement: int, emplacement_value: int,
                        type_to_place: str) -> list[list[str]]:
    ...

def three_case_winning(board: list[list[str]], number_of_recurence: int) -> tuple[bool, str]:
    ...

def print_board(board: list[list[str]]) -> None:
    ...

def player_turn(board: list[list[str]], player_token: str, number_of_occurence_to_win: int) -> tuple[list[list[str]], tuple[bool, str]]:
    ...

def board_creation(size: int) -> list[list[str]]:
    ...

def main() -> None:
    ...

