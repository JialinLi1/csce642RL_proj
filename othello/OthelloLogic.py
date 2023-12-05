'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''

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

import numpy as np

class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            # the second entry denotes obstacle. use separate data point to avoid unwanted linearity
            self.pieces[i] = [(0,0)]*self.n 

        # Set up the initial 4 pieces.
        c1 = int(self.n/2)-1
        c2 = int(self.n/2)
        self.pieces[c1][c2] = (1,0)
        self.pieces[c2][c1] = (1,0)
        self.pieces[c1][c1] = (-1,0)
        self.pieces[c2][c2] = (-1,0)
    
        # set up random at most obs obstacles
        obs = self.n // 2
        for i in range(obs):
            a = np.random.randint(self.n)
            b = np.random.randint(self.n)
            # starting places cannot be obstacles
            if not ((a==c1 or a==c2) and (b==c1 or b==c2)):
                # remember the second entry of self.pieces[a][b] is the obstacle
                self.pieces[a][b] = (0,1)


    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y][0]==color:
                    count += 1
                if self[x][y][0]==-color:
                    count -= 1
        return count

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y][0]==color and self[x][y][1]==0: # make sure to exclude obstacle squares
                    newmoves = self.get_moves_for_square((x,y))
                    moves.update(newmoves)
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y][0]==color and self[x][y][1]==0: # make sure to exclude obstacle squares
                    newmoves = self.get_moves_for_square((x,y))
                    if len(newmoves)>0:
                        return True
        return False

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        That is, if the given square is (3,4) and it contains a black piece,
        and (3,5) and (3,6) contain white pieces, and (3,7) is empty, one
        of the returned moves is (3,7) because everything from there to (3,4)
        is flipped.
        """
        (x,y) = square

        # determine the color of the piece.
        color = self[x][y][0]

        # skip empty source squares and obstacle squares
        if color==0 or self[x][y][1] != 0:
            return None

        # search all possible directions.
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                # print(square,move,direction)
                moves.append(move)

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        #Much like move generation, start at the new piece's square and
        #follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)
        flips = [flip for direction in self.__directions
                      for flip in self._get_flips(move, direction, color)]
        # print(len(list(flips)))
        if len(list(flips))==0: 
            print(move)
            print(self.pieces)
        assert len(list(flips))>0
        for x, y in flips:
            #print(self[x][y][0],color)
            assert self[x][y][1] == 0
            self[x][y] = (color,0)

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin
        color = self[x][y][0]
        flips = []

        for x, y in Board._increment_move(origin, direction, self.n):
            if self[x][y][0] == 0 and self[x][y][1] == 0:
                if flips:
                    # print("Found", x,y)
                    return (x, y)
                else:
                    return None
            elif self[x][y][0] == color:
                return None
            elif self[x][y][0] == -color:
                # print("Flip",x,y)
                flips.append((x, y))
            # New: if hit an obstacle, then this is deadend, stop
            elif self[x][y][1] != 0: # should be == 1, why doesn't work? it's multiplied by -1 at some point?
                return None

    def _get_flips(self, origin, direction, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        #initialize variables
        flips = [origin]

        for x, y in Board._increment_move(origin, direction, self.n):
            # print(x,y)
            if self[x][y][0] == 0 or self[x][y][1] != 0:
                return []
            if self[x][y][0] == -color:
                flips.append((x, y))
            elif self[x][y][0] == color and len(flips) > 0:
                #print(flips)
                return flips

        return []

    @staticmethod
    def _increment_move(move, direction, n):
        # print(move)
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        #move = (move[0]+direction[0], move[1]+direction[1])
        while all(map(lambda x: 0 <= x < n, move)): 
        #while 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
            yield move
            move=list(map(sum,zip(move,direction)))
            #move = (move[0]+direction[0],move[1]+direction[1])

