//Alpha Beta Pruning for tic tac toe

#include <iostream>
#include <iomanip>
#include <algorithm>
#include <chrono>

//Time Algorithm
std::chrono::high_resolution_clock::time_point start;
std::chrono::high_resolution_clock::time_point finish;
std::chrono::duration<double> elapsed;

//Print Current Status of Board
void printBoard(int _board[][3]) {
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            std::cout << _board[i][j] << "  ";
            if(j != 2) std:: cout << "|  ";
        }
        if(i!= 2) std::cout << "\n--------------\n";
        else std::cout << std::endl;
    }
}

int checkWin(int _board[][3])
{
    for(int i = 0; i < 3; i++) 
        if(_board[i][0] == _board[i][1] && _board[i][1] == _board[i][2] && _board[i][0] != 0) {
            return _board[i][0];
        }
    for(int i = 0; i < 3; i++)
        if(_board[0][i] == _board[1][i] && _board[1][i] == _board[2][i] && _board[0][i] != 0){
            return  _board[0][i];
        }
    if(_board[0][0] == _board[1][1] && _board[1][1] == _board[2][2] && _board[0][0] != 0) return _board[0][0]; 
    if(_board[0][2] == _board[1][1] && _board[1][1] == _board[2][0] && _board[0][2] != 0) return _board[0][2];
    return 0;
}
int evaluate(int _board[][3])
{
    //Winning Player
    int winner = -1; 
    //Horizontal
    for(int i = 0; i < 3; i++) 
        if(_board[i][0] == _board[i][1] && _board[i][1] == _board[i][2] && _board[i][0] != 0) {
            winner = _board[i][0];
            break;
        }
    //Vertical 
    for(int i = 0; i < 3; i++)
        if(_board[0][i] == _board[1][i] && _board[1][i] == _board[2][i] && _board[0][i] != 0){
            winner = _board[0][i];
            break;
        }
    //Diagonals
    if(_board[0][0] == _board[1][1] && _board[1][1] == _board[2][2] && _board[0][0] != 0) winner = _board[0][0]; 
    if(_board[0][2] == _board[1][1] && _board[1][1] == _board[2][0] && _board[0][2] != 0) winner = _board[0][2];
   
    //Return Points
    if(winner == 2) return 10;
    else if(winner == 1) return -10;
    else return 0;    
}

int alpha_beta_pruning(int _board[][3], int _depth, int _alpha, int _beta, bool _isMax)
{
    int score = evaluate(_board);
    if(score == 10) return score - _depth; //Heuristic --> prioritize shorter amount of wins
    else if(score == -10) return score + _depth; 

    //If there are no more moves left and is a tie
    bool movesLeft = false;
    for(int i = 0; i < 3 && !movesLeft; i++)
        for(int j = 0; j < 3 && !movesLeft; j++) {
            if (_board[i][j] == 0) movesLeft = true;
        }    
    if(!movesLeft) return 0;
    //Max Player
    if(_isMax) {
        int best = - 1000;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if(_board[i][j] == 0) {
                    _board[i][j] = 2; //DFS through possible moves
                    best = std::max(best, alpha_beta_pruning(_board, _depth+1, _alpha, _beta, !_isMax));
                    _alpha = std::max(_alpha, best);
                    _board[i][j] = 0;
                    if(_beta <= _alpha) break;
                }
            }
        }
        return best;
    }
    else {
        int best = 1000;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if(_board[i][j] == 0) {
                    _board[i][j] = 1; //Simulate if I was making my move
                    best = std::min(best, alpha_beta_pruning(_board, _depth+1, _alpha, _beta, !_isMax));
                    _beta = std::min(_beta, best);
                    _board[i][j] = 0; 
                    if(_beta <= _alpha) break;
                }   
            }
        }
        return best;
    }
}
void pickBestMove(int _board[][3])
{
    int bestValuedMove = -1000;
    int bestMoveRow = -1;
    int bestMoveCol = -1;
    int alpha = -1000000;
    int beta = 1000000;
    auto start = std::chrono::high_resolution_clock::now();
    //Traverse all empty cells, evaluate alpha-beta-pruning for each empty cell and find the most optimal one
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            if(_board[i][j] == 0) {
                _board[i][j] = 2; // Computer makes best move
                int moveVal = alpha_beta_pruning(_board, 0, alpha, beta, false);
                _board[i][j] = 0;
                if(bestValuedMove < moveVal) {
                    bestMoveRow = i;
                    bestMoveCol = j;
                    bestValuedMove = moveVal;
                }
            } 
        }
    }
    auto finish = std::chrono::high_resolution_clock::now();
    elapsed = finish - start;
    std::cout << elapsed.count() << std::endl;
    _board[bestMoveRow][bestMoveCol] = 2;
}

void playGame(int _board[][3])
{
    int count = 0;
    int moveX;
    int moveY;
    
    while(count < 9) {
        printBoard(_board);
        std::cout << "Your Turn! ";
        bool validMove = false;
        while(!validMove) {
            std::cin >> moveX >> moveY;
            if(_board[moveX][moveY] == 0 && moveX < 3 && moveY < 3) {
                _board[moveX][moveY] = 1;
                validMove = true;
            }
            else std::cout << "Invalid Move!\n";
        }
        if(checkWin(_board) != 0) {
            printBoard(_board);
            std::cout << "Hooman Wins!\n";
            break;
        }
        std::cout << "Computer Turn\n";
        pickBestMove(_board);
        if(checkWin(_board) !=0) {
            printBoard(_board);
            std::cout << "Compooter Wins!\n";
            break;
        }
        count+=2;        
    }
    if(count > 9) std::cout << "It's a tie :C";
}
int main(int argc, char** argv) {
    std::cout << "This is Alphebeta-Algorithm Bot \n Try to beat me! \n";
    int board[3][3] = {0};
    playGame(board);

}
