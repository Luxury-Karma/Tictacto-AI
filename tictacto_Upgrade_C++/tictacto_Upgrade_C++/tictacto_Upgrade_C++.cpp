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

int** applyMove(int playerToken, int** board, int row, int col) {
    board[row][col] = playerToken;
    return board;
}


void printBoard(int** board, int boardSize) {
    for (int i = 0; i < boardSize; i++) {
        for (int j = 0; j < boardSize; j++) {
            std::cout << "| " << board[i][j] << "| ";
        }
        std::cout << "\n";
    }

}

int main()
{
    int boardSize = 3;
    // initial playing board
    int** board = create2DArray(boardSize);
    
    // player board Tokens
    const int playerAmount = 2;
    int player[playerAmount];
    player[0] = 1; 
    player[1] = 2;
    board = applyMove(player[0], board, 0, 0);
    printBoard(board, boardSize);









    
}
