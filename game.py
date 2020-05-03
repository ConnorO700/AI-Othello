from graphics import *
import math
from tile import *
from agents import *
from GameState import *
class Board:

    def drawMatrix(self, matrix):
        space = 100 #space at the top of the screen
        for row in range(0,8):
            for col in range(0,8):
                pt1 = Point(100*col +10*col + 10, 100*row + 10*row + space)
                pt2 = Point(pt1.x + 100, pt1.y + 100)
                t = Tile(pt1,pt2, matrix[row][col])
                t.drawTile(self.win)


    def __init__(self, win_inp, A, agent1 = None, agent2 = None):
        self.winner = 0
        self.player = 1 #1 = white; 2 = black
        self.Ai1 = agent1
        self.Ai2 = agent2
        self.isGameOver = False
        self.win = win_inp
        self.gameState = GameState(A)
        space = 100 #space at the top of the screen
        #self.drawMatrix(self.gameState.getMatrix())


    def getMoveFromAI(self):
        if self.player == 1:
            return self.getMoveFromAI1()
        else:
            return self.getMoveFromAI2()
    def getMoveFromAI1(self):
        temp = deepcopy(self.gameState)
        return self.Ai1.getAction(temp)
    def getMoveFromAI2(self):
        temp = deepcopy(self.gameState)
        return self.Ai2.getAction(temp)

    def gameOver(self):
        self.isGameOver = True
        wScore = self.gameState.getWhiteScore()
        bScore = self.gameState.getBlackScore()
        if wScore == bScore:
            #print("tie")
        elif wScore > bScore:
            self.winner = 1
            #print("white wins")
        elif wScore  < bScore:
            self.winner = 2
            #print("black wins")
        else: #never gets here
            print("nobody wins")
            print("shouldn't be possible to get here! congrats!")
        #print("score: ", wScore, " to ", bScore)


    def getWinner(self):
        return self.winner


    """
    detects player click on the board and attempts to flipTiles
    """
    def playerVsPlayer(self):
        actions = self.gameState.getLegalActions(self.player)
        if len(actions) == 0:
            self.gameOver()
        else:
            click = self.win.getMouse()
            col = math.floor(click.x/110)
            row = math.floor(click.y/110)-1
            action = (row, col)
            if action in actions:
                self.gameState = self.gameState.generateSuccessor(self.player, action)
                #self.drawMatrix(self.gameState.getMatrix())
                self.player = self.player % 2 + 1 #switches player turn between 1 and 2

    def playerVsAgent(self):
        if self.player == 1:
            self.playerVsPlayer() #human will always be player 1
        else:
            actions = self.gameState.getLegalActions(self.player)
            if len(actions) == 0:
                self.gameOver()
            elif len(actions) == 1: #only 1 move possible skip AI
                self.gameState = self.gameState.generateSuccessor(self.player,actions[0])
                self.player = self.player % 2 + 1 #switches player turn between 1 and 2
            else:
                action = self.getMoveFromAI1()
                if action in actions:
                    print("this action:", action)
                    #self.gameState.printGameState()
                    self.gameState = self.gameState.generateSuccessor(self.player,action)
                    #self.drawMatrix(self.gameState.getMatrix())
                    self.player = self.player % 2 + 1 #switches player turn between 1 and 2
                else:
                    print("illegal actions!")
                    print("action:", action, " was not found in:", actions)
                    self.gameState.printGameState()
                    self.isGameOver = True

    def agentVsAgent(self):
        actions = self.gameState.getLegalActions(self.player)
        if len(actions) == 0:
            self.gameOver()
        elif len(actions) == 1: #only 1 move possible skip AI
            self.gameState = self.gameState.generateSuccessor(self.player,actions[0])
            self.player = self.player % 2 + 1 #switches player turn between 1 and 2
        else:
            action = self.getMoveFromAI()#automatically gets the move from the correct AI
                                        #so there is no need to check for player
            if action in actions:
                self.gameState = self.gameState.generateSuccessor(self.player,action)
                #self.drawMatrix(self.gameState.getMatrix())
                self.player = self.player % 2 + 1 #switches player turn between 1 and 2
            else:
                print("illegal actions!")
                print("action:", action, " was not found in:", actions)
                self.gameState.printGameState()
                self.isGameOver = True






    #def getNextState(self, move)


    def drawPlayer(self):
        if not self.isGameOver:
            labelw = Text(Point(400,50), "White:" + str(self.gameState.getWhiteScore()))
            labelb = Text(Point(600,50), "Black:" + str(self.gameState.getBlackScore()))
            if self.player == 1:
                label = Text(Point(102,50), "Turn: White")

            else:
                label = Text(Point(100,50), "Turn: Black")
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

    def drawBoard(self):
        self.drawPlayer()
        self.drawMatrix(self.gameState.getMatrix())

class Game:
    def __init__(self, win, B, agent1=None, agent2=None):
        self.agent1 = agent1
        self.agent2 = agent2
        self.win = win
        self.player1Wins = 0
        self.player2Wins = 0
        self.tie = 0
        self.board = Board(win, deepcopy(B),agent1, agent2)
        self.A = B


    def getPlayer1Wins(self):
        print(self.agent1.getName(), "has won :", self.player1Wins)

    def getPlayer2Wins(self):
        print(self.agent2.getName(), "has won :", self.player2Wins)

    def getTie(self):
        print("Ties:", self.tie)



    def guantlet(self, rounds):
        for x in range(0,rounds):
            self.board.drawBoard()
            while(True):
                self.board.agentVsAgent()
                self.board.drawBoard()
                if self.board.isGameOver:
                    winner = self.board.getWinner()
                    if winner == 1:
                        self.player1Wins = self.player1Wins + 1
                    elif winner == 2:
                        self.player2Wins = self.player2Wins + 1
                    else:
                        self.tie = self.tie + 1
                    break

            self.board = Board(self.win, deepcopy(self.A),self.agent1, self.agent2)


    def guantletNoGraphics(self, rounds):
        for x in range(0,rounds):
            while(True):
                self.board.agentVsAgent()
                if self.board.isGameOver:
                    winner = self.board.getWinner()
                    if winner == 1:
                        self.player1Wins = self.player1Wins + 1
                    elif winner == 2:
                        self.player2Wins = self.player2Wins + 1
                    else:
                        self.tie = self.tie + 1
                    break
            self.board = Board(self.win, deepcopy(self.A),self.agent1, self.agent2)



def main():
    #import sys
    #print(sys.version)
    win = GraphWin("Othello", 900, 1000)
    win.setBackground('black')
    A = [   [0,0,0,0,0,0,0,0], #tile matrix for handling graphics
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]   ]
    #AI takes a max depth and a player number and a name
    rm1 = RandomAI(3,1, "random agent1")
    rm2 = RandomAI(3,2, "random agent2")
    ab1 = AlphaBetaAI(3,1, "alphaB agent1")
    ab2 = AlphaBetaAI(1,2, "alphaB agent2")
    em1 = ExpectimaxAI(3,1, "expectiM agent1")
    em2 = ExpectimaxAI(3,2, "expectiM agent2")
    #em = AI(2,3) #AI takes a player number and a max depth
    #b = Board(win, A, ab, rm)
    #d = Board(win,A, ab, rm)
    g = Game( win, A, rm1, em2)
    #g.guantlet(2)
    g.guantletNoGraphics(100)
    g.getPlayer1Wins()
    g.getPlayer2Wins()
    g.getTie()
    win.close()



    """
    #b.drawPlayer()
    while(True):
        b.agentVsAgent()
        #b.drawPlayer()
        if b.isGameOver:
            break

    win.close()
    """
main()
