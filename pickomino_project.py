from utils import *

class Rewards:
    C = 0
    R = [0 for i in range(21)] + [1 + i // 4 for i in range(16)]


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


class State:

    def __init__(self, keptDices, remainingDices):
        # keptDices : tuple of length 6 that indicates how many dice i the player has kept
        # remainingDices : similar
        assert(len(keptDices) == 6 and len(remainingDices) == 6)
        assert(sum(keptDices) + sum(remainingDices) == 8)
        self.keptDices = keptDices
        self.remainingDices = remainingDices
        self.possibleActions = []

        self.is_final = self.possibleActions == set({})

    
    def __str__(self):
        keptDices = []
        remainingDices = []

        # adding worms
        for j in range(self.keptDices[dice_value]):
            keptDices.append("W")
        for j in range(self.remainingDices[dice_value]):
            remainingDices.append("W")
        
        # adding regular dices
        for dice_value in range(1, 6):
            for j in range(self.keptDices[dice_value]):
                keptDices.append(dice_value)
            for j in range(self.remainingDices[dice_value]):
                remainingDices.append(dice_value)

        #Converting back keptDice and remainingDice to tuples to fit the announced types
        keptDices = tuple(keptDices)
        remainingDices = tuple(remainingDices)
        return "Kept dices : " + str(keptDices) + " Remaining dices : " + str(remainingDices)
            
    def is_final_state(self):
        # returns true iff state is final ; that is no dice can be picked
        # the boolean value is_final is computed at init for performance reasons
        return self.is_final

    def get_kept_value(self):
        # assuming player chooses to stop immediately, how many points do they have ?
        if self.keptDices[0] == 0: # player did not keep a worm : failed !
            return Rewards.C
        if self.is_final:
            return Rewards.C

        #Counting the number of points given by the worms 
        dices_sum = 5 * self.keptDices[0]
        #Counting the number of points given by the others dice faces
        for dice_value in range(1, 6):
            dices_sum += self.keptDices[dice_value] * dice_value
        if dices_sum < 21:
            return Rewards.C
        #If sum is over the max usable sum, use it at this maximum.
        #Attention not to keep this when doing part 2.
        if dices_sum > len(Rewards.R):
            dices_sum = len(Rewards.R) - 1
        return Rewards.R[dices_sum]
        

def reward(s : State, a):
    if a != Action.STOP:
        return 0 # reward is 0 for intermediate states (where player chooses to continue)
    
    return s.get_kept_value()