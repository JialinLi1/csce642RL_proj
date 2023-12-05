# Playing Othello-with-Obstacles using Alpha Zero like Algorithm

Class project for CSCE 642 Reinforcement Learning by Jialin Li

Othello-with-Obstacles: like a normal Othello game, but there are several obstacles scattered throughout the board. You cannot place a piece on cells with obstacles, and they do not contribute toward game rules. They simply stand in your way.

Therefore, you should adjust your strategy to capture the stable cells at not only the corner, but around the obstacles as well (if any)

### Credits

This project is based on Alpha Zero General by Surag Nair and other contributors (2016). It has the games, the MCTS algorithm and the neural networks defined for multiple games. 

I have changed the core logic in the game implementation as well as configurations of the algorithm and neural network to support my version of the game: Othello-with-Obstacles.

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
```bash
python  train.py
```
This will start training using Monte-Carlo tree search. It is set to be running 100 episodes per iteration and 25 MCTS simulations per turn. You can modify ```train.py``` to have it train on a 6x6 board or an 8x8 board.

However due to constraints of time and resources, I only have one 6x6 model trained. This model is the result of 25 iterations, and while not the most powerful agent yet, it is much more powerful than random or simple greedy players.

To play, do
```
python play.py
```
and you can specify which version (6x6 or 8x8) as well as who's playing (human against computer or computer vs computer). Currently there is only a model for the 6x6 Othello, and you can play against it. 
