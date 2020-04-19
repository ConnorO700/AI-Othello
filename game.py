from graphics import *
import math
class Tile:
    def __init__(self, topleft, botright, given):
        self.rect = Rectangle(topleft,botright)
        self.rect.setFill('green')
        width = abs(topleft.x - botright.x)
        height = abs(topleft.y - botright.y)
        pnt_CTR = Point(topleft.x + width/2, topleft.y+height/2)
        self.circ = Circle(pnt_CTR,width/2)
        self.color = given  #0 = none
                            #1 = white
                            #2 = black
        if self.color == 1:
            self.circ.setFill('white')
            self.circ.setOutline('black')
        elif self.color == 2:
            self.circ.setFill('black')
            self.circ.setOutline('white')

    def drawTile(self, win):
        self.rect.undraw()
        self.rect.draw(win)
        if(self.color):
            self.circ.undraw()
            self.circ.draw(win)

    def flipTile(self, win):
        if self.color == 0:
            return 0
        elif self.color == 1:
            self.color = 2
            self.circ.setFill('black')
            self.circ.setOutline('white')
        elif self.color == 2:
            self.color = 1
            self.circ.setFill('white')
            self.circ.setOutline('black')
        self.drawTile(win)


    def setTile(self, color, win):
        if self.color == 0:
            self.color = color
            if color == 2:
                self.circ.setFill('black')
                self.circ.setOutline('white')
            elif color == 1:
                self.circ.setFill('white')
                self.circ.setOutline('black')
            self.drawTile(win)

class Board:

    def drawMatrix(self, matrix):
        space = 100 #space at the top of the screen
        for row in range(0,8):
            for col in range(0,8):
                pt1 = Point(100*col +10*col + 10, 100*row + 10*row + space)
                pt2 = Point(pt1.x + 100, pt1.y + 100)
                t = Tile(pt1,pt2, matrix[row][col])
                t.drawTile(self.win)

    def __init__(self, win_inp):
        self.player = 1 #1 = white; 2 = black
        self.whiteScore = 2
        self.blackScore = 2
        self.win = win_inp
        self.A = [  [0,0,0,0,0,0,0,0], #tile matrix for handling graphics
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,1,2,0,0,0],
                    [0,0,0,2,1,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]]
        space = 100 #space at the top of the screen
        self.drawMatrix(self.A)
        #self.A[row][col] = t

    def getGameState(self):
        return self.A
    """
    @param last last matrix index
    @param dx step values through matrix in the x direction
    @param dy step values through matrix in the y direction
    @param color int value of tile color
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

        tilesToFlip = tilesToFlip + self.pathStep(move, 0,-1,color,[]) #north
        tilesToFlip = tilesToFlip + self.pathStep(move, 1,-1,color,[]) #northeast
        tilesToFlip = tilesToFlip + self.pathStep(move, 1,0,color,[]) #east
        tilesToFlip = tilesToFlip + self.pathStep(move, 1,1,color,[]) #southeast
        tilesToFlip = tilesToFlip + self.pathStep(move, 0,1,color,[]) #south
        tilesToFlip = tilesToFlip + self.pathStep(move, -1,1,color,[]) #southwest
        tilesToFlip = tilesToFlip + self.pathStep(move, -1,0,color,[]) #west
        tilesToFlip = tilesToFlip + self.pathStep(move, -1,-1,color,[]) #northwest

        if len(tilesToFlip) != 0:
            tilesToFlip = tilesToFlip + [(move[0], move[1])]
        return tilesToFlip



    """
    flips a given list of tiles

    @param flippedTiles list of tiles to flip
    @param color of the player who is flipping

    @returns matrix boardstate
    """
    def flipfunc(self, flippedTiles, color):
        B = self.A
        if color == 1:
            self.whiteScore = self.whiteScore + len(flippedTiles) + 1
            self.blackScore = self.blackScore - len(flippedTiles)
        elif  color == 2:
            self.blackScore = self.blackScore + len(flippedTiles) + 1
            self.whiteScore = self.whiteScore - len(flippedTiles)
        for x in range(0,len(flippedTiles)):
            B[flippedTiles[x][0]][flippedTiles[x][1]] = color

            #flippedTiles[x].flipTile(self.win)
        return B


    """
    detects player click on the board and attempts to flipTiles
    """
    def getMoveFromPlayer(self):
        click = self.win.getMouse()
        col = math.floor(click.x/110)
        row = math.floor(click.y/110)-1
        if self.A[row][col] == 0: #players can only potentially select green tiles to move
            tiles = self.gatherTiles((row,col),self.player)
            if len(tiles) != 0:
                self.A = self.flipfunc(tiles, self.player)
                self.drawMatrix(self.A)
                self.player = self.player%2 + 1 #switches player turn

    """
    gameState.getLegalActions(agentIndex):
    Returns a list of legal actions for an agent
    agentIndex=0 means Pacman, ghosts are >= 1

    gameState.generateSuccessor(agentIndex, action):
    Returns the successor game state after an agent takes an action
    """

    def getNextMoves(self, player):
        moves = []
        for i in range(0,8):
            for j in range(0,8):
                if self.A[i][j].color == 0:
                    tiles = gatherTiles((i,j), player)



    #def getNextState(self, move)

    def drawPlayer(self):
        labelw = Text(Point(400,50), "White:" + str(self.whiteScore))
        labelb = Text(Point(600,50), "Black:" + str(self.blackScore))
        if self.player == 1:
            label = Text(Point(100,50), "Turn: White")

        else:
            label = Text(Point(50,50), "Turn: Black")
        rect = Rectangle(Point(0,0),Point(900,100))
        rect.setFill('black')
        rect.draw(self.win)
        label.setTextColor('white')
        label.setSize(30)
        label.draw(self.win)
        labelw.setTextColor('white')
        labelw.setSize(30)
        labelw.draw(self.win)
        labelb.setTextColor('white')
        labelb.setSize(30)
        labelb.draw(self.win)


    """
    This function helps the evaluationFunction by evaluating an individual
    tile based on the position and who owns it. returning -10, -3, -1, 0, 1, 3, 10

    @param tile int 0 =none, 1 =white, 2 =black
    @param max int  the max index for row and or col in a square matrix
    @param x, y tile position in the given state

    @return value of that tile based off color and position; black = min white =max
    """
    def evaluateTile(self,tile, max, x, y):
        if tile == 0:
            return 0
        row = x % max #only zero if 0th row or max row
        col = y % max #only zero if 0th col or max col
        eval = -((tile*2) -3) #this converts 1=white 2=black into 1=white -1 =black
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
    def evaluationFunction(self, gameState):
        max = len(gameState)
        score = 0
        for x in range(0,max):
            for y in range(0, max):
                score = score + self.evaluateTile(gameState[x][y], max-1, x, y)
        return score

def main():
    import sys
    print(sys.version)
    win = GraphWin("Othello", 900, 1000)
    win.setBackground('black')
    b = Board(win)
    b.drawPlayer()
    while(True):
        b.getMoveFromPlayer()
        b.drawPlayer()
        print(b.evaluationFunction(b.getGameState()))
    win.close()
main()
