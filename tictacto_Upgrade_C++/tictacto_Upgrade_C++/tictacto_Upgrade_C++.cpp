// tictacto_Upgrade_C++.cpp : Ce fichier contient la fonction 'main'. L'exécution du programme commence et se termine à cet endroit.
//

#include <iostream>
const int emptyCell = 0;

// Create a 2D Array that will be the playing board. The empty tiles are 0
int** create2DArray(int arraySize)
{
    int** arr = new int* [arraySize];
    for (int i = 0; i < arraySize; i++)
    {
        arr[i] = new int[arraySize];
        for (int j = 0; j < arraySize; j++)
        {
            arr[i][j] = emptyCell;
        }
    }

    return arr;
}


// Apply a modification to a 2D array
int** applyMove(int playerToken, int** board, int row, int col) {
    board[row][col] = playerToken;
    return board;
}

// Show the board on CMD
void printBoard(int** board, int boardSize) {
    for (int i = 0; i < boardSize; i++) {
        for (int j = 0; j < boardSize; j++) {
            std::cout << "| " << board[i][j] << "| ";
        }
        std::cout << "\n";
    }

}

// Give the user the choice of the movement
//TODO: ENSURE THE CELL IS EMPTY
//TOOD: ENSURE THE INPUT IS AN INTEGER
int* playerMovement() {
    int answer[2];
    std::cout << "Enter the row ";
    std::cin >> answer[0];
    std::cout << "You entered the row: " << answer[0] << std::endl;

    std::cout << "Enter the col: ";
    std::cin >> answer[1];
    std::cout << "You entered the row: " << answer[1] << std::endl;

    return answer;
}


// Look for an horizontal win condition (same line)
// it look from left to right
int* horizontalWin(int** board, int boardSize, int rowToLook, int cellToLook, int amountToWin) 
{
    int winner[2];
    winner[0]= 1;
    winner[1] = board[rowToLook][cellToLook];
    //Ensure that we can win
    if ((amountToWin+cellToLook) < (boardSize)) {
        for (int i = 1; i <= amountToWin; i++) {
            // Look if we don't win
            if (board[rowToLook][cellToLook] != board[rowToLook][i + cellToLook]) {
                winner[0] = emptyCell;
                winner[1] = emptyCell;
                return winner;
            }
        }
    }
    else {
        winner[0] = emptyCell;
        winner[1] = emptyCell;
    }
    return winner;
}

// Look for a Vertical Win condition (same row)
// It look from top to botom
int* verticalWin(int** board, int boardSize, int rowToLook, int cellToLook, int amountToWin) {
    int winner[2];
    winner[0] = 1;
    winner[1] = board[rowToLook][cellToLook];
    if ((rowToLook + amountToWin) < boardSize) {
        for (int i = 1; i <= amountToWin; i++) {
            if (board[rowToLook][cellToLook] != board[i + rowToLook][cellToLook]) {
                winner[0] = 0;
                winner[1] = 0;
                return winner;
            }
        }
    }
    else
    {
        winner[0] = 0;
        winner[1] = 0;
    }
    return winner;
}

// Look for angle (right to left) conditions
int* leftToRightAngleWin(int** board, int boardSize, int rowToLook, int cellToLook, int amountToWin) {
    int winner[2];
    winner[0] = 1;
    winner[1] = board[rowToLook][cellToLook];
    if ((rowToLook + amountToWin) < boardSize && (cellToLook + amountToWin) < boardSize) 
    {
        for (int i = 1; i <= amountToWin; i++) {
            if (board[rowToLook][cellToLook] != board[rowToLook + i][cellToLook + i])
            {
                winner[0] = emptyCell;
                winner[1] = emptyCell;
                return winner;
            }
        }
    }
    else {
        winner[0] = emptyCell;
        winner[1] = emptyCell;
    }

    return winner;
}
// Look for a angle (left to right) conditions
int* rightToLeftAngleWin(int** board, int boardSize, int rowToLook, int cellToLook, int amountToWin) {
    int winner[2];
    winner[0] = 1;
    winner[1] = board[rowToLook][cellToLook];
    if ((rowToLook - amountToWin) >= 0 && (cellToLook - amountToWin) >= 0) {
        for (int i = 1; i <= amountToWin; i++) {
            if (board[rowToLook][cellToLook] != board[rowToLook - i][cellToLook - i]) {
                winner[0] = emptyCell;
                winner[1] = emptyCell;
                return winner;
            }
        }
    }
    else
    {
        winner[0] = emptyCell;
        winner[1] = emptyCell;
    }

    return winner;
}

/*
FOR ALL WINNING CONDITION
it will return a 0 or 1 at position 0 to say if there is or not a winner, and also at position 1 the token (number) of the winning player
*/
// Check for all winning conditions
int* Winning_Conditions(int** board, int boardSize, int amountToWin) {
    // Loop in all cells of the board
    int* winner = new int[2];
    winner[0] = emptyCell;
    winner[1] = emptyCell;
    amountToWin = amountToWin - 1;
    for (int i = 0; i < boardSize; i++) 
    {
        for (int j = 0; j < boardSize; j++) 
        {
            // need to pass all the conditions
            if (board[i][j] != emptyCell) 
            {
                
                winner = horizontalWin( board, boardSize, i, j, amountToWin);
                if (winner[0] != emptyCell) {
                    return winner;
                }
                winner = verticalWin(board, boardSize, i, j, amountToWin);
                if (winner[0] != emptyCell) {
                    return winner;
                }
                winner = leftToRightAngleWin(board, boardSize, i, j, amountToWin);
                if (winner[0] != emptyCell) {
                    return winner;
                }
                winner = rightToLeftAngleWin(board, boardSize, i, j, amountToWin);
                if (winner[0] != emptyCell) {
                    return winner;
                }
                
            }
        }
    }
    return winner;
}


int main()
{
    // initial playing board
    int boardSize = 3;
    int** board = create2DArray(boardSize);
    int amountToWin = 3;
    bool playing = 1;
    
    // player Tokens
    const int playerAmount = 2;
    int player[playerAmount];
    player[0] = 1; 
    player[1] = 2;
    int playerIndex = 0;


    //initial board
    printBoard(board, boardSize);
    while (playing)
    {
 
        // player turn
        int* movement = playerMovement();

        // apply the movement
        board = applyMove(player[playerIndex], board, movement[0], movement[1]);
        // remove for memory 

        printBoard(board, boardSize);

        //look for winning conditions
        int* winner = Winning_Conditions(board, boardSize, amountToWin);
        if (winner[0] != emptyCell) {
            std::cout << "Player " << winner[1] << " WIN";
            playing = 0;
            continue;
        }

        // Insure that the player don't break index and switch players
        playerIndex++;
        if (playerAmount <= playerIndex) {
            playerIndex = 0;
        }



    }





    
}
