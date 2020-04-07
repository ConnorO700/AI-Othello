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
    def __init__(self, win_inp):
        self.player = 1 #1 = white; 2 = black
        self.white = 2
        self.black = 2
        self.win = win_inp
        self.A = [  [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,1,2,0,0,0],
                    [0,0,0,2,1,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]]
        space = 100 #space at the top of the screen
        for row in range(0,8):
            for col in range(0,8):
                pt1 = Point(100*col +10*col + 10, 100*row + 10*row + space)
                pt2 = Point(pt1.x + 100, pt1.y + 100)
                t = Tile(pt1,pt2, self.A[row][col])
                t.drawTile(self.win)
                self.A[row][col] = t


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
                currTile = self.A[currdy][currdx]
                if(currTile.color != color and currTile.color != 0 ):
                    found = found + [currTile]
                    return self.pathStep(currp, dx, dy, color, found)
                elif(currTile.color == color):
                    len(found)
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
    @param move indices(point) in matrix where a player is attmepting to place a new tile
    @color color of the player who is moving

    @returns color player (if illegal move will return same player w/o flipping tiles)
    """
    def flipfunc(self, move, color):
        flippedTiles = []

        flippedTiles = flippedTiles + self.pathStep(move, 0,-1,color,[]) #north
        flippedTiles = flippedTiles + self.pathStep(move, 1,-1,color,[]) #northeast
        flippedTiles = flippedTiles + self.pathStep(move, 1,0,color,[]) #east
        flippedTiles = flippedTiles + self.pathStep(move, 1,1,color,[]) #southeast
        flippedTiles = flippedTiles + self.pathStep(move, 0,1,color,[]) #south
        flippedTiles = flippedTiles + self.pathStep(move, -1,1,color,[]) #southwest
        flippedTiles = flippedTiles + self.pathStep(move, -1,0,color,[]) #west
        flippedTiles = flippedTiles + self.pathStep(move, -1,-1,color,[]) #northwest
        """
        print("north", self.pathStep(move, 0,-1,color,[])) #north
        print("northeast", self.pathStep(move, 1,-1,color,[])) #northeast
        print("east", self.pathStep(move, 1,0,color,[])) #east
        print("southeast", self.pathStep(move, 1,1,color,[])) #southeast
        print("south", self.pathStep(move, 0,1,color,[])) #south
        print("southwest", self.pathStep(move, -1,1,color,[])) #southwest
        print("west", self.pathStep(move, -1,0,color,[])) #west
        print("northwest", self.pathStep(move, -1,-1,color,[])) #northwest
        """


        if len(flippedTiles) != 0:
            if color == 1:
                self.white = self.white + len(flippedTiles) + 1
                self.black = self.black - len(flippedTiles)
            elif  color == 2:
                self.black = self.black + len(flippedTiles) + 1
                self.white = self.white - len(flippedTiles)
            for x in range(0,len(flippedTiles)):
                flippedTiles[x].flipTile(self.win)
            self.A[move[0]][move[1]].setTile(color, self.win)
            return True

        else:
            return False
            #this move isn't allowed pick again

    def getMove(self):
        click = self.win.getMouse()
        col = math.floor(click.x/110)
        row = math.floor(click.y/110)-1
        if self.A[row][col].color == 0:
            if self.flipfunc((row,col), self.player):
                self.player = self.player%2 + 1 #switches player turn


    def drawPlayer(self):
        labelw = Text(Point(400,50), "White:" + str(self.white))
        labelb = Text(Point(600,50), "Black:" + str(self.black))
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

def main():
    import sys
    print(sys.version)
    win = GraphWin("Othello", 900, 1000)
    win.setBackground('black')
    b = Board(win)
    b.drawPlayer()
    while(True):
        b.getMove()
        b.drawPlayer()
    win.close()
main()
