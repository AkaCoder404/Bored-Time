# Bored-Time
This repository contains code for small projects that I have pursued. It contains test code to learn different algorithms and how they can be applied such as the A and A* algorithm for maze solving and solving the 8-puzzle.


## Codes and Their Descriptions

### 8 Puzzle Solver 
Solves the traditional 8 puzzle game. User inputs the initial board and the program utilizes the A* path finding algorithm to find the shortest way of solving the puzzle. The hueristic used is the manhatten hueristic. Assumes user inputs are correct.

Improvements: 1. interface

### Maze Solver
Finds the shortest path from a starting point in a maze to the ending point. User inputs initial maze width and height and the starting position. Then, walls are automatically generated randomly, the probability of a wall generated can be changed by manipulating '''if(random.randint(0,100) < SOME_VALUE)'''. Then the program uses the A* path finding algorithm and ecludian distance hueristic to find the shortest path through the maze. 

Improvements: 1. interface 2. customizability by user: percentage of walls 3. code is a bit messy 
