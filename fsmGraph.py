class Vertex:
    def __init__(self,state):
        self.state = state
        self.nbrs = set()

    # condition is the condition required to move from
    # current vertex to the nbr
    def addNeighbor(self,nbr,condition):
        self.nbrs.add((nbr,condition))

    def getNeighbors(self,condition=None):
        if condition:
            nbrs = set()
            for i in self.nbrs:
                if i[1] == condition:
                    nbrs.add(i[0])
            return nbrs
        else:
            return self.nbrs

    def selective_neighbors(self,condition,known):
        selective_paths = set()
        possiblePaths = self.getNeighbors(condition)
        for i in possiblePaths:
            if i not in known:
                selective_paths.add(i)
        return selective_paths
        

    def printPaths(self):
        out = set()
        for i in self.nbrs:
            out.add((str(i),i[1]))
        return out
         
    def getState(self):
        return self.state
    
    def __str__(self):
        return self.state
