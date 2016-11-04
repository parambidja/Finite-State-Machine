from fsmGraph import Vertex

class FSM:
    def __init__(self):
        self.currentState = None
        self.startState = None
        self.acceptStates = set()
        self.states = {}
        
    # statename is a string, the name of state
    def setstartstate(self, statename):
        if statename in self.states:
            self.startState = self.states[statename]
        else:
            self.startState = Vertex(statename)
            self.states[statename] = self.startState
            
        self.currentState = self.startState
            
        
    # Adds the state named StateName to the set of accept states.
    # That state must already by one of the states
    def setacceptstate(self, statename):
        if statename in self.states:
            self.acceptStates.add(statename)
        else:
            raise ValueError(statename + " does not exist as a State.")
            
    # Adds the state named StateName to the FSM.
    def addstate(self, statename):
        self.states[statename] = Vertex(statename)

    # fromstate and tostate are the strings labeling the states in the transition.  
    # label should be a single character.
    def addtransition(self, fromstate, tostate, label):
        self.states[fromstate].addNeighbor(self.states[tostate],label)

    # Return true if and only if the FSM accepts string.
    def accepts(self, currentString,currentState=None):
        if not self.startState:
            raise ValueError("A start state has not been defined.")

        if not currentState:
            currentState = self.currentState
            
        if not currentString:  # base case - empty string
            return currentState.getState() in self.acceptStates
        
        possibleStates = currentState.getNeighbors(currentString[0:1])
        for i in possibleStates:  # traverse all possible paths
            if self.accepts(currentString[1:],i): # if any call results in True, return True
                return True
        return False


    

            
            
    

