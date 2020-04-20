#include <iostream>
#include <iomanip>
#include <time.h>
#include <algorithm>
#include <chrono>
#include <cstring>

#define MAX(a, b) ((a) > (b)) ? (a) : (b))
#define MIN(a, b) ((a) < (b)) ? (a) : (b))

using namespace std;
//Limit Time of Node Searching (althouh not completely necessary for this because its relatively small)
std::chrono::high_resolution_clock::time_point start;
std::chrono::high_resolution_clock::time_point finish;
std::chrono::duration<double> elapsed;

// Implement the MiniMax algorithm - recursive and backtracking alroithm usually used in game theory
// 1 - Player
// 2 - Opponent
// 0 - Empty Space
//Make A pretty Table
template<typename T> void printElement(T t, const int& width) {
    cout << left << setw(width) << setfill(' ') << t;
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
//Evaluate if there is a winner
int evaluate(int _board[][3], int _depth) {
    int best = -1;
    //Horizontal
    for(int i = 0; i < 3; i++) 
        if(_board[i][0] == _board[i][1] && _board[i][1] == _board[i][2] && _board[i][0] != 0) {
            best = _board[i][0];
            break;
        }
    //Vertical
    for(int i = 0; i < 3; i++)
        if(_board[0][i] == _board[1][i] && _board[1][i] == _board[2][i] && _board[0][i] != 0){
            best = _board[0][i];
            break;
        }
    //Diagonal
    if(_board[0][0] == _board[1][1] && _board[1][1] == _board[2][2] && _board[0][0] != 0) best = _board[0][0]; 
    if(_board[0][2] == _board[1][1] && _board[1][1] == _board[2][0] && _board[0][2] != 0) best = _board[0][2];

    //Return Points - our heuristic (total points 10 - depth (how many moves it takes to win))
    if(best == 2) return 10; 
    else if(best == 1) return -10;
    else return 0;
}
//Minmax algorithm returns best valued move
int miniMax(int _board[][3], int _depth, int _isMax)
{
    int score = evaluate(_board, _depth);
   
    //if max wins else if min wins
    if(score == 10) return score - _depth;
    else if (score == -10) return score + _depth;

    //if there are no moves left and its a tie - no one gets points
    bool movesLeft = false;
    for(int i = 0; i < 3 && !movesLeft; i++)
        for(int j = 0; j < 3 && !movesLeft; j++){
            if (_board[i][j] == 0) movesLeft = true;
        }
    if(!movesLeft) return 0;   

    if(_isMax) {
        int best = -1000;
        auto finish = std::chrono::high_resolution_clock::now();
        elapsed = finish - start;
        for(int i = 0; i < 3; i++) {
            for(int j = 0; j < 3; j++) {
                if(_board[i][j] == 0 && elapsed.count() < 10) {
                    _board[i][j] = 2;//ai to make best move
                    best = max(best, miniMax(_board, _depth+1, !_isMax));
                    _board[i][j] = 0;
                }
                else if (elapsed.count() >= 10)
                {
                    return best;
                }
            }
        }
        return best;   
    }
    else {
        int best = 1000;
        auto finish = std::chrono::high_resolution_clock::now();
        elapsed = finish - start;
        for(int i = 0; i <3; i++) {
            for(int j = 0; j < 3; j++) {
                //elapsed.count() is not necessary due to relatively small game variations of tic tac toe
                if(_board[i][j] == 0 && elapsed.count() < 10) {
                    _board[i][j] = 1; //simulate if i were to make move
                    best = min(best, miniMax(_board, _depth+1, !_isMax));
                    _board[i][j] = 0;
                }
                else if (elapsed.count() >= 10)
                {
                    return best;
                }
            }
        }
        return best;   
    }   
}
int pickBestMove(int _board[][3], int *_moveCount)
{
    int bestValue = -1000;
    int bestMoveRow = -1;
    int bestMoveCol = -1;
    //Traverse all cells, evaluate miniMax for all of them, and return cell with optimal value
    start = std::chrono::high_resolution_clock::now();
    for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
            if(_board[i][j] == 0) {
                _board[i][j] = 2; //Computer makes best move
                int moveVal = miniMax(_board, 0, false);
                _board[i][j] = 0;
                if(moveVal > bestValue) {
                    bestMoveRow = i;
                    bestMoveCol = j;
                    bestValue = moveVal;
                }
            }
        }
    }
    auto finish = std::chrono::high_resolution_clock::now();
    elapsed = finish - start;
    _board[bestMoveRow][bestMoveCol] = 2;
    (*_moveCount)++;
    cout << elapsed.count() << endl;
}

void playGame(int _board[][3], int *_moveCount)
{
    int moveX;
    int moveY;
    
    while((*_moveCount) < 9) {
        cout << "Computer Turn\n";
        pickBestMove(_board, _moveCount);
        for(int i = 0; i < 3; i++) {
            for(int j = 0; j <3; j++) {
                printElement(int(_board[i][j]), 2);
                if(j != 2) printElement('|', 2); 
            }
            if(i != 2) cout << "\n----------\n";    
        }
        cout << endl;
        if(checkWin(_board) != 0) {

            cout << "Computer Wins!";
            break;
        }
        cout << "Your turn! ";
        bool validMove = false;
        while(!validMove) {
            cin >> moveX >> moveY;
            if(_board[moveX][moveY] == 0){
                _board[moveX][moveY] = 1;
                validMove = true;
            }
            else {
                cout << "Invalid Move!\n";
            }
        }        
        (*_moveCount)++;  
        cout << endl;
        if(checkWin(_board) != 0) {
            cout << "Human Wins!";
            break;
        }
    }
    if(*_moveCount == 9) cout << ("It's a tie!");
}

int main(int argc, char** argv)
{
    cout << "This is MiniMax Bot\nYou are player 1\n";
    int board[3][3] = {0};    
    int moveX = 0;
    int moveY = 0;
    cout << "First Move ";
    cin >> moveX >> moveY;
    board[moveX][moveY] = 1;
    int moveCount = 1;
    playGame(board, &moveCount); 
  
}
