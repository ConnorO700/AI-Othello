from graphics import *
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
