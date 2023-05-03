import os
def clear_screen():
    if (os.name == 'posix'):
        os.system('clear')
    # else screen will be cleared for windows
    else:
        os.system('cls')


def save_file(path: str, files: [[str]]) -> None:
  """
  Save a multilayer array into a file
  :param path: Where the file should be save
  :param files: Data of the file
  :return: None
  """
  with open(path, 'w', encoding="utf-8") as save:
    for e in files:
      for k in e:
        save.write(f'{k}\n')
    save.close()


def print_board(board):
    index: int = 1
    for e in board:
        if index == 1:
            temp_array = []
            number_of_cell = 1
            for i in range(len(e)):
                temp_array.append(f'{number_of_cell}')
                number_of_cell = number_of_cell + 1
            print(f'{0}: {temp_array}')

        print(f'{index}: {e}')
        index = index + 1


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