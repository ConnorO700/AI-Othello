
from copy import *
class GameState:

    def __init__(self, B):
        self.A = B
        self.whiteScore = 0
        self.blackScore = 0
        for row in range(0,8):
            for col in range(0,8):
                if self.A[row][col] == 1:
                    self.whiteScore = self.whiteScore + 1
                if self.A[row][col] == 2:
                    self.blackScore = self.blackScore + 1

    def printGameState(self):
        for row in range(0,8):
            print(self.A[row])
        print("Current Score: w:", self.whiteScore, " to  b:", self.blackScore)

    def getMatrix(self):
        return self.A

    def setMatrix(self, B):
        self.A = B

    def getGameState(self):
        return copy(self)

    def setGameState(self,B):
        self = B

    def getNumAgents(self):
        return 2

    def getWhiteScore(self):
        return self.whiteScore

    def getBlackScore(self):
        return self.blackScore



    def isGameOver(self):
        white = self.getLegalActions(1)
        black = self.getLegalActions(2)
        if white == None or black == None:
            return True
        else:
            return False

    """
    @param last last matrix index
    @param dx step values through matrix in the x direction
    @param dy step values through matrix in the y direction
    @param color int value of player color
    @param found list consecutive of enemy colored tiles inbetween your tile and your move

    @return list of tiles you capture

    """
    def pathStep(self,last,dx, dy, color, found):
        #print("last",last)
        currdx = last[1] + dx
        currdy = last[0] + dy
        currp = (currdy,currdx)
        #print("next:", currp)
        if -1 < currdx and currdx < 8:
            if -1 < currdy and currdy < 8:
                currTileColor = self.A[currdy][currdx]
                if(currTileColor != color and currTileColor != 0 ):
                    found = found + [currp]
                    return self.pathStep(currp, dx, dy, color, found)
                elif(currTileColor == color):
                    return found
                else:
                    found.clear()
                    return found
            else:
                found.clear()
                return found
        else:
            found.clear()
            return found

    """
    given a move finds a list of tiles to flip

    @param move indices(point) in matrix where a player is attmepting to place a new tile
    @param color of the player who is moving

    @returns list of tiles to be flipped
    """
    def gatherTiles(self, move, color):
        tilesToFlip = []
        #West and east are fine, but north and south are inverted
        tilesToFlip = tilesToFlip + self.pathStep(move, 0,-1,color,[]) #north
        tilesToFlip = tilesToFlip + self.pathStep(move, 1,-1,color,[]) #northeast
        tilesToFlip = tilesToFlip + self.pathStep(move, 1,0,color,[]) #east
        tilesToFlip = tilesToFlip + self.pathStep(move, 1,1,color,[]) #southeast
        tilesToFlip = tilesToFlip + self.pathStep(move, 0,1,color,[]) #south
        tilesToFlip = tilesToFlip + self.pathStep(move, -1,1,color,[]) #southwest
        tilesToFlip = tilesToFlip + self.pathStep(move, -1,0,color,[]) #west
        tilesToFlip = tilesToFlip + self.pathStep(move, -1,-1,color,[]) #northwest

        if len(tilesToFlip) != 0:
            tilesToFlip = tilesToFlip + [move]
        #print("color", color)
        #print(tilesToFlip)
        return tilesToFlip

    """
    gameState.getLegalActions(agentIndex):
    Returns a list of legal actions for an agent
    agentIndex=0 means Pacman, ghosts are >= 1

    """
    def getLegalActions(self, color):
        moves = []
        for i in range(0,8):
            for j in range(0,8):
                if self.A[i][j] == 0:
                    tiles = self.gatherTiles((i,j), color)
                    if len(tiles) != 0:
                        moves = moves + [(i,j)]
        return moves
    """
    flips a given list of tiles

    @param flippedTiles list of tiles to flip
    @param color of the player who is flipping

    @returns matrix boardstate
    """
    def flipFunc(self, flippedTiles, color):
        #B = self.A
        if color == 1:
            self.whiteScore = self.whiteScore + len(flippedTiles)
            self.blackScore = self.blackScore - len(flippedTiles) + 1
        elif  color == 2:
            self.blackScore = self.blackScore + len(flippedTiles)
            self.whiteScore = self.whiteScore - len(flippedTiles) + 1
        for x in range(0,len(flippedTiles)):
            self.A[flippedTiles[x][0]][flippedTiles[x][1]] = color

            #flippedTiles[x].flipTile(self.win)
        #return B


    """
    gameState.generateSuccessor(agentIndex, action):
    Returns the successor game state after an agent takes an action
    """
    def generateSuccessor(self, color, action):
        newGameState = copy(self)
        if action != None:
            if newGameState.A[action[0]][action[1]] == 0: #players can only potentially select green tiles to move
                tiles = newGameState.gatherTiles((action[0],action[1]), color)
                if len(tiles) != 0:
                    newGameState.flipFunc(tiles, color)
        return newGameState


    """ ***NOTE: go back and assign significantly higher value on making a winning move***
    This function helps the evaluationFunction by evaluating an individual
    tile based on the position and who owns it. returning -10, -3, -1, 0, 1, 3, 10


    @param tile int 0 =none, 1 =white, 2 =black
    @param max int  the max index for row and or col in a square matrix
    @param x, y tile position in the given state

    @return value of that tile based off color and position; black = min white =max
    """
    def evaluateTile(self,tile, max, x, y, color):
        if tile == 0:
            return 0
        row = x % max #only zero if 0th row or max row
        col = y % max #only zero if 0th col or max col
        eval = 0
        if tile == color:
            eval = 1
        else:
            eval = -1
        if not row and not col:
            #print("both")
            return eval*10
        elif not row:
            #print("row")
            return eval*3
        elif not col:
            #print("col")
            return eval*3
        else:
            return eval

    """
    iterates through the gameState summing the value of every tile

    @param gameState the matrix A

    @return sum of every tiles evaluation

    """
    def evaluationFunction(self, color):
        max = len(self.A)
        score = 0
        for x in range(0,max):
            for y in range(0, max):
                score = score + self.evaluateTile(self.A[x][y], max-1, x, y, color)
        return score
