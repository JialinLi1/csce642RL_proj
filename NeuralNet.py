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

class NeuralNet():
    """
    This class specifies the base NeuralNet class. To define your own neural
    network, subclass this class and implement the functions below. The neural
    network does not consider the current player, and instead only deals with
    the canonical form of the board.

    See othello/NNet.py for an example implementation.
    """

    def __init__(self, game):
        pass

    def train(self, examples):
        """
        This function trains the neural network with examples obtained from
        self-play.

        Input:
            examples: a list of training examples, where each example is of form
                      (board, pi, v). pi is the MCTS informed policy vector for
                      the given board, and v is its value. The examples has
                      board in its canonical form.
        """
        pass

    def predict(self, board):
        """
        Input:
            board: current board in its canonical form.

        Returns:
            pi: a policy vector for the current board- a numpy array of length
                game.getActionSize
            v: a float in [-1,1] that gives the value of the current board
        """
        pass

    def save_checkpoint(self, folder, filename):
        """
        Saves the current neural network (with its parameters) in
        folder/filename
        """
        pass

    def load_checkpoint(self, folder, filename):
        """
        Loads parameters of the neural network from folder/filename
        """
        pass
