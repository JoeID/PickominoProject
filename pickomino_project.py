from utils import *

class Rewards: # it's a global variable but prettier
    C = 0
    R = [0 for i in range(21)] + [1 + i // 4 for i in range(16)] + [4 for i in range(4)]


class Action:    
    
    def __init__(self, stop : bool, value):
        '''There are 3 types of action : 
            -pick a value V of a rolled dice to keep and continue
                (represented by stop = False and value = V)
            -pick a value of a rolled dice to keep and take the highest value domino reacheable
                (represented by stop = True and value = V)
            -loose your turn
                (represented by stop = True and value = None)'''
        self.stop = stop
        self.value = value

    def __str__(self):
        return "("+str(self.stop)+","+str(self.value)+")"
    
    def __hash__(self):
        return hash((self.stop,self.value))
    
    def __eq__(self, other):
        return (self.stop, self.value) == (other.stop, other.value)

class State:

    def __init__(self, keptDices, remainingDices):
        # keptDices : tuple of length 6 that indicates how many dice i the player has kept
        # remainingDices : similar
        assert(len(keptDices) == 6 and len(remainingDices) == 6)
        #assert(sum(keptDices) + sum(remainingDices) == 8)
        self.keptDices = keptDices
        self.remainingDices = remainingDices
        #It is often unecessary to compute the possibles actions
        self.possibleActions = None

    def get_possibleActions(self):
        if self.possibleActions is None:
        #If not already done, compute the possible actions from the state
            self.possibleActions = set()
            for i in range(6):
                if self.keptDices[i] == 0 and self.remainingDices[i] != 0:
                    self.possibleActions.add(Action(True,i))
                    self.possibleActions.add(Action(False,i))
            if self.possibleActions == set():
                self.possibleActions.add(Action(True,None))
        #In any case, return the set of possible actions
        return self.possibleActions
    
    def __str__(self):
        return str((str(self.keptDices), str(self.remainingDices))) 
    
    def __hash__(self):
        return hash((self.keptDices,self.remainingDices))
    
    def __eq__(self, other):
        return (self.keptDices, self.remainingDices) == (other.keptDices, other.remainingDices)