'''
This part of the code has been provided by Surag Nair and others for general Alpha(Go) Zero implementation
and has been adapted to implement Jialin Li's Othello with Obstacles

Added support for obstacles on the board
Players cannot place pieces on obstacles,
and they do not contribute to the game rule tests

To remove unwanted linearity, the obstacle is represented 
as an additional dimension to the board

The neural network has been modified too in order to accept this new configuration

Improved and Augmented by Jialin Li
Texas A&M University
Nov 30, 2023
'''

'''
This part is taken as is, and I only changed certain configurations to fit my implementation
'''

import Arena
from MCTS import MCTS
from othello.OthelloGame import OthelloGame
from othello.OthelloPlayers import *
from othello.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

mini_othello = True  # Play in 6x6 instead of the normal 8x8.
human_vs_cpu = False

if mini_othello:
    g = OthelloGame(6)
else:
    g = OthelloGame(8)

# all players
rp = RandomPlayer(g).play
gp = GreedyOthelloPlayer(g).play
hp = HumanOthelloPlayer(g).play



# nnet players
n1 = NNet(g)
if mini_othello:
    n1.load_checkpoint('./trained_models/','checkpoint_25.pth.tar')
else:
    raise "Currently only support 6x6 mini othello games"
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./trained_models/','checkpoint_25.pth.tar')
    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=OthelloGame.display)

print(arena.playGames(2, verbose=True))
