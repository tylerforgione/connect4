# Connect 4 AI

## Overview

This is a connect 4 AI opponent using minimax. The minimax algorithm is depth-limited, uses a transposition table, move-ordering, and has alpha-beta pruning.
The graphical interface was made in PyGame so as to not have to play in the console. The game has a menu so that you may choose whether to play as yellow or red.

## Setup

To run this game, download both files (runner.py and connect4.py) and install all dependencies. Use "pip install pygame" in the terminal to install PyGame.
If you are running this in PyCharm, make sure to install it through that. Obviously, if in PyCharm, just press run on runner.py.
If in the terminal, run runner.py while in the directory with the two files. My directory is called connect4, so I "cd ~/connect4" and then "python runner.py"

## How to Play

Connect4 rules are all the same as the real game. Red goes first and pieces always fall to the lowest row they can fall to in a given column. First to get 4 in a row wins.
Use the mouse to slide the checker over the column you'd like to place it in. Left click to let it drop. This will trigger the AI move. When the game ends, you may press R to restart.

## Algorithm

This AI uses the basic recursive minimax algorithm. This algorithm flip flops between two helper functions, max_value and min_value, which try to maximize and minimize the score.
The red player will always have a positive score and the yellow player a negative score. If the AI is yellow, it will play moves which minimize the score.
To do this, minimax allows the AI to play out moves as both red and yellow in order to find the optimal move down the line. 
If a move gives the AI 3 in a row now, but next turn allows the player to win, it will not play that move.

### What is minimax?
Minimax works in this way essentially: if the AI is red, it will call max_value, which will call min_value (since the next turn yellow plays) which will call max_value and so on.
This goes until the end of the game or until the depth limit is reached. Each recursive call of the helper functions returns a value that represents the score of the best move that player could make.
So, max_value tries to choose the move that gives the highest score, assuming that the opponent will choose a move that gives the lowest score.
NOTE: The reason the algorithm is called minimax is because it tries to minimize the maximum loss.
This will lead to the AI playing the move that helps itself the most if the player were to play the optimal move after it.

### Depth-limiting
My depth has been set to 7, however the algorithm works faster and just as well with a depth down to 4. Using a depth of 7 gives an average move time of 2 seconds.
Using a depth of 4 gives an average move time of 0.1 seconds. This is at no cost to performance, although I am not good at connect 4.

#### Evaluation Function
Since the algorithm doesn't reach the end of the game, I needed to use an evaluation function. This function is quite simple.
It checks each possible scoring window (4 spaces) and returns a score based on the number of checkers are within that window with an empty space.
Having 3 checkers with an empty space is 50 points, having 2 checkers and 2 empty spaces would be 20 points, and having 1 checker would be 5 points.
In the event that the minimax algorithm does reach the end of the game (if it's late in the game), my utility function defines wins in less turns as more valuable.
This doesn't matter however, as within my minimax function, I make it always choose a winning move before anything, if available.

### Alpha-beta Pruning
Since Connect 4 is quite a large game-space, I opted to use alpha-beta pruning. This basically makes it so that the algorithm does not check paths which are proven to be worse.
In the max_value function, let's assume I've found some score. If, on the next loop I have 3 paths, all of which are worse (lower scores than I have already), I won't continue the recursive calls.
Same goes for the min_value fucntion.

### Move-ordering
I've also implemented move-ordering. Instead of my minimax algorithm looking through all the possible moves, I order the moves in terms of priority. 
Highest priority goes to winning moves, then moves that block the opponent from winning, then moves that create threats (3 in a row), and then the rest.
Because of the way Connect 4 is designed, the center columns are worth more, so this is factored into priority.
This makes it so that the minimax algorithm searches through the best moves first (instead of random) and, paired with alpha-beta pruning, this saves a ton of search time.

### Transposition table
A transposition table is a cache (or hash table) that stores previously calculated board states and the best move from there.
The idea is that, in Connect 4, you can arrive at the same board position a number of different ways. How you got there doesn't matter, the best move is still the same.
The transposition table saves an entire minimax search if the board state has already been calculated.
This works better at higher depth values for the minimax algorithm since greater depth means more boards seen.
