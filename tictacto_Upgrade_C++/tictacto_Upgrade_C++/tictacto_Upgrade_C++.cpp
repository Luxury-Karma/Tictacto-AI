// tictacto_Upgrade_C++.cpp : Ce fichier contient la fonction 'main'. L'exécution du programme commence et se termine à cet endroit.
//

#include <iostream>


// Create a 2D Array that will be the playing board. The empty tiles are 0
int** create2DArray(int arraySize)
{
    int** arr = new int* [arraySize];
    for (int i = 0; i < arraySize; i++)
    {
        arr[i] = new int[arraySize];
        for (int j = 0; j < arraySize; j++)
        {
            arr[i][j] = 0;
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


int main()
{
    int boardSize = 3;
    // initial playing board
    int** board = create2DArray(boardSize);
    bool playing = 1;
    
    // player board Tokens
    const int playerAmount = 2;
    int player[playerAmount];
    player[0] = 1; 
    player[1] = 2;
    int playerIndex = 0;
    while (playing)
    {
 
        // player turn
        int* movement = playerMovement();

        // apply the movement
        board = applyMove(player[playerIndex], board, movement[0], movement[1]);
        // remove for memory 
        delete movement;


        //look for winning conditions

        // Insure that the player don't break index and switch players
        playerIndex++;
        if (playerAmount <= playerIndex) {
            playerIndex = 0;
        }



    }





    
}
