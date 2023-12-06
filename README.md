# Playing Othello-with-Obstacles using Alpha(Go) Zero

Class project for CSCE 642 Reinforcement Learning by Jialin Li

Video Link: https://youtu.be/xanhzDkyMXA

Othello-with-Obstacles: like a normal Othello game, but there are several obstacles scattered throughout the board. You cannot place a piece on cells with obstacles, and they do not contribute toward game rules. They simply stand in your way.

Therefore, you should adjust your strategy to capture the stable cells at not only the corner, but around the obstacles as well (if any).

### Credits

This project is based on Alpha Zero General by Surag Nair and other contributors (2016). It has the games, the MCTS algorithm and the neural networks defined for multiple games. 

The Othello game implementation is due to Eric P. Nichols. 

I have changed part of the core logic in the game implementation as well as configurations of the algorithm and neural network to support my version of the game: Othello-with-Obstacles. Lastly, I modified the PyTorch neural network configurations to make it utilize multiple GPUs.

### Requirements

It's recommended to use Anaconda to set up an environment for the program. It requires, among others,
```
python
numpy
torch
cuda (if applicable)
tqdm
coloredlogs
```
```torch``` and ```cuda``` needs to be installed using anaconda directly, and others can be installed through ```pip```, which should pull up any other needed packages. If you install these packages manually, it should also install all their dependencies automatically.

### Training and Playing
To start training a model for Othello:
```
python  train.py
```
This will start training using Monte-Carlo tree search. It is set to be running 100 episodes per iteration and 25 MCTS simulations per turn. You can modify ```train.py``` to have it train on a 6x6 board or an 8x8 board.

However due to constraints of time and resources, I only have one 6x6 model trained. This model is the result of 25 iterations, and while not the most powerful agent yet, it is smarter than random or simple greedy agents.

To play, do
```
python play.py
```
and you can specify which version (6x6 or 8x8) as well as who's playing (human against computer or computer vs computer). Currently there is only a model for the 6x6 Othello, and you can play against it. If you play against the computer, the program will start 2 games back to back. The first game have you play the black and the second white. **White moves first.**

**The game is text based.** The program will simply print the current board on the console as well as a list of valid moves for you. To make a move, simply put in the coordinate as denoted in 2 numbers.

White:       O
Black:       @
Obstacle:    X
Empty cell:  -

```
Turn  6 Player  -1
   0 1 2 3 4 5
-----------------------
0 |- - @ - X X |
1 |- - - @ - O |
2 |- - @ O O - |
3 |- - O O O - |
4 |- - - - - - |
5 |X - - - - - |
-----------------------
[ 2 5] [ 3 5] [ 4 2] [ 4 3] [ 4 4]
```

In this example state you are playing black (as denoted by Player -1), and the valid moves are provided to you. If you type ```3 5``` and press enter, you will place a move at **row** 3 and **column** 5, as denoted by the board, resulting in the next board state: 
```
Turn  7 Player  1        <-- now it's white's turn, in this case computer
   0 1 2 3 4 5
-----------------------
0 |- - @ - X X |
1 |- - - @ - O |
2 |- - @ O @ - |
3 |- - O O O @ |         <-- you have placed at row 3, column 5
4 |- - - - - - |
5 |X - - - - - |
-----------------------
```

When neither player has any more valid moves, the game ends, and whoever has the more pieces win, just like regular Othello.
