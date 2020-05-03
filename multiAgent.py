"""
class Agent:

    #An agent must define a getAction method, but may also define the
    #following methods which will be called if they exist:

    #def registerInitialState(self, state): # inspects the starting state


    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):

        #The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        #must return an action from Directions.{North, South, East, West, Stop}

        raiseNotDefined()
"""

class MultiAgentSearchAgent:
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, board, index=2, depth = '2'):
        self.board = board
        self.index = index
        self.depth = int(depth)

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        raiseNotDefined()
    def argMax(self, gameState):
        pass
    def argMin(self, gameState):
        pass


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #action, temp = self.argMax(gameState, self.depth)
        #print("action taken:", action, "\n score: ", temp)
        pacman = 0
        possibleActions = gameState.getLegalActions(pacman)
        action = None
        highValue = float("-inf")
        for actionIndex in range(0,len(possibleActions)):
            potentialState = gameState.generateSuccessor(pacman, possibleActions[actionIndex])
            currValue = self.minimax(potentialState, 0, 0)
            if highValue <= currValue:
                highValue = currValue
                action = possibleActions[actionIndex]
        #print("max picked:", highValue)
        return action

        util.raiseNotDefined()

    """
    minimax takes arguements:
		gameState = the board you play on/ map
		currDepth = depth of the searchTree where 1 depth is max->min->max with any number of min steps inbetween max steps always calling state eval before the final max step
		isGhost = int player index where max = 0 and min = Everything else

    minimax returns int of the gameState(board) evaluation according to a min-max tree

    this minimax function uses helper code before it is called to find the best action instead of the best state evaluation
    """
    def minimax(self,gameState, currDepth, isGhost):
        isGhost = isGhost + 1 				#increment isGhost
        isGhost = isGhost % gameState.getNumAgents()	#check if isGhost has rolled over aka isGhost = 0
        if gameState.isLose() or gameState.isWin():	#in win or lose state
            return self.board.evaluationFunction(gameState)
        if not isGhost: #then is pacman agent
            currDepth = currDepth + 1
            if currDepth == self.depth:			#max depth reached
                return self.evaluationFunction(gameState)
            highValue = float("-inf")
            pacman = 0	#I could use isGhost here but I use pacman instead to make code more readable
            possibleActions = gameState.getLegalActions(pacman) #pacman always 0
            for actionIndex in range(0,len(possibleActions)):
                potentialState = gameState.generateSuccessor(pacman, possibleActions[actionIndex])
                currValue = self.minimax(potentialState, currDepth, isGhost)
                highValue = max(highValue, currValue)
            return highValue
        else: #ghost agent
            lowValue = float("inf")
            possibleActions = gameState.getLegalActions(isGhost) #one ghost for now
            for actionIndex in range(0, len(possibleActions)):
                potentialState = gameState.generateSuccessor(isGhost, possibleActions[actionIndex])
                currValue = self.minimax(potentialState, currDepth, isGhost)
                lowValue = min(lowValue, currValue)
            return lowValue



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pacman = 0
        possibleActions = gameState.getLegalActions(pacman)
        action = None
        highValue = float("-inf")
        lowValue = float("inf")
        for actionIndex in range(0,len(possibleActions)):
            potentialState = gameState.generateSuccessor(pacman, possibleActions[actionIndex])
            currValue = self.alphaBeta(potentialState, 0, 0, highValue, lowValue)
            if highValue < currValue:
                highValue = currValue
                action = possibleActions[actionIndex]
        #print("max picked:", highValue)
        return action

        util.raiseNotDefined()
    def alphaBeta(self,gameState, currDepth, isGhost, alpha, beta):
        isGhost = isGhost + 1 				#increment isGhost
        isGhost = isGhost % gameState.getNumAgents()	#check if isGhost has rolled over aka isGhost = 0
        if gameState.isLose() or gameState.isWin():	#in win or lose state
            return self.board.evaluationFunction(gameState)
        if not isGhost: #max func
            currDepth = currDepth + 1
            if currDepth == self.depth:			#max depth reached
                return self.evaluationFunction(gameState)
            value = float("-inf")
            pacman = 0	#I could use isGhost here but I use pacman instead to make code more readable
            possibleActions = gameState.getLegalActions(pacman) #pacman always 0
            for actionIndex in range(0,len(possibleActions)):
                potentialState = gameState.generateSuccessor(pacman, possibleActions[actionIndex])
                value = max(value, self.alphaBeta(potentialState, currDepth, isGhost, alpha, beta ))
                alpha = max(alpha, value)
                if alpha > beta:
                    break;
            return value
        else: #min func
            value = float("inf")
            possibleActions = gameState.getLegalActions(isGhost) #one ghost for now
            for actionIndex in range(0, len(possibleActions)):
                potentialState = gameState.generateSuccessor(isGhost, possibleActions[actionIndex])
                value = min(value, self.alphaBeta(potentialState, currDepth, isGhost, alpha, beta))
                beta = min(beta, value)
                if beta < alpha:
                    break;
            return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacman = 0
        depthStart = 0
        possibleActions = gameState.getLegalActions(pacman)
        action = None
        highValue = float("-inf")
        for actionIndex in range(0,len(possibleActions)):
            potentialState = gameState.generateSuccessor(pacman, possibleActions[actionIndex])
            currValue = self.expectimax(potentialState, depthStart, pacman)
            if highValue < currValue:
                highValue = currValue
                action = possibleActions[actionIndex]
        #print("max picked:", highValue)
        return action


        util.raiseNotDefined()
    def expectimax(self, gameState, currDepth, player):
        player = player + 1 				        #increment isGhost
        player = player % gameState.getNumAgents()	#check if isGhost has rolled over aka isGhost = 0
        if gameState.isLose() or gameState.isWin():	#in win or lose state
            return self.evaluationFunction(gameState)
        if not player: #max function
            currDepth = currDepth + 1
            if currDepth == self.depth:			#max depth reached
                return self.evaluationFunction(gameState)
            highValue = float("-inf")
            possibleActions = gameState.getLegalActions(player)
            for actionIndex in range(0,len(possibleActions)):
                potentialState = gameState.generateSuccessor(player, possibleActions[actionIndex])
                highValue = max(highValue,  self.expectimax(potentialState, currDepth, player))
            return highValue
        else: #expectation function
            possibleActions = gameState.getLegalActions(player)
            probability = 1/len(possibleActions)
            expectation = 0
            for actionIndex in range(0, len(possibleActions)):
                potentialState = gameState.generateSuccessor(player, possibleActions[actionIndex])
                #discrete expectation = sum(Xn*Pn)
                expectation = expectation + self.expectimax(potentialState, currDepth, player) * probability
            return expectation
