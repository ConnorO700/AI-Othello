import time
import random

class AI:
    def __init__(self, maxDepth, playerNum, name):
        self.sleeper = 0 #sleep time between ai moves
        self.player = playerNum
        self.depth = maxDepth
        self.name = name

    def getName(self):
        return self.name

class RandomAI(AI):
    def getAction(self, gameState):
        time.sleep(self.sleeper)
        moves = gameState.getLegalActions(self.player)
        rand = random.randint(0,len(moves)-1)
        return moves[rand]

class AlphaBetaAI(AI):
    def getAction(self, gameState):
        time.sleep(self.sleeper)
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        possibleActions = gameState.getLegalActions(self.player)
        action = possibleActions[0]
        highValue = float("-inf")
        lowValue = float("inf")
        for actionIndex in range(0,len(possibleActions)):
            potentialState = gameState.generateSuccessor(self.player, possibleActions[actionIndex])
            currValue = self.alphaBeta(potentialState, 0, self.player, highValue, lowValue)
            if highValue < currValue:
                highValue = currValue
                action = possibleActions[actionIndex]
        return action

        util.raiseNotDefined()
    def alphaBeta(self,gameState, currDepth, isPlayer, alpha, beta):
        isPlayer = (isPlayer % 2) + 1
        if gameState.isGameOver():	#in win or lose state
            #print("gameover?")
            return gameState.evaluationFunction(self.player)
        if isPlayer == self.player: #max func
            currDepth = currDepth + 1
            if currDepth == self.depth:			#max depth reached
                return gameState.evaluationFunction(self.player)
            value = float("-inf")
            player = self.player	#I could use isPlayer here but I use player instead to make code more readable
            possibleActions = gameState.getLegalActions(self.player)
            for actionIndex in range(0,len(possibleActions)):
                potentialState = gameState.generateSuccessor(self.player, possibleActions[actionIndex])
                value = max(value, self.alphaBeta(potentialState, currDepth, isPlayer, alpha, beta ))
                alpha = max(alpha, value)
                if alpha > beta:
                    break;
            return value
        else: #min func
            value = float("inf")
            possibleActions = gameState.getLegalActions(isPlayer)
            for actionIndex in range(0, len(possibleActions)):
                potentialState = gameState.generateSuccessor(isPlayer, possibleActions[actionIndex])
                value = min(value, self.alphaBeta(potentialState, currDepth, isPlayer, alpha, beta))
                beta = min(beta, value)
                if beta < alpha:
                    break;
            return value

class ExpectimaxAI(AI):
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        depthStart = 0
        possibleActions = gameState.getLegalActions(self.player)
        action = None
        highValue = float("-inf")
        for actionIndex in range(0,len(possibleActions)):
            potentialState = gameState.generateSuccessor(self.player, possibleActions[actionIndex])
            currValue = self.expectimax(potentialState, depthStart, self.player)
            if highValue < currValue:
                highValue = currValue
                action = possibleActions[actionIndex]
        #print("max picked:", highValue)
        return action


        util.raiseNotDefined()
    def expectimax(self, gameState, currDepth, player):
        player = (player % 2) + 1 				        #increment isPlayer
        if gameState.isGameOver():
            return gameState.evaluationFunction(self.player)
        if player == self.player: #max function
            currDepth = currDepth + 1
            if currDepth == self.depth:			#max depth reached
                return gameState.evaluationFunction(self.player)
            highValue = float("-inf")
            possibleActions = gameState.getLegalActions(self.player)
            for actionIndex in range(0,len(possibleActions)):
                potentialState = gameState.generateSuccessor(self.player, possibleActions[actionIndex])
                highValue = max(highValue,  self.expectimax(potentialState, currDepth, player))
            return highValue
        else: #expectation function
            possibleActions = gameState.getLegalActions(player)
            if len(possibleActions) == 0:
                return gameState.evaluationFunction(self.player)
            probability = 1/len(possibleActions)
            expectation = 0
            for actionIndex in range(0, len(possibleActions)):
                potentialState = gameState.generateSuccessor(player, possibleActions[actionIndex])
                #discrete expectation = sum(Xn*Pn)
                expectation = expectation + self.expectimax(potentialState, currDepth, player) * probability
            return expectation
