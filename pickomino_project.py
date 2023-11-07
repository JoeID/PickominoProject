import utils

class Rewards:
    C = 0
    R = [0 for i in range(21)] + [1 + i // 4 for i in range(16)]


class Action:
    STOP = 0


class State:

    def __init__(self, keptDices, remainingDices):
        # keptDices : tuple of length 6 that indicates how many dice i the player has kept
        # remainingDices : similar
        assert(len(keptDices) == 6 and len(remainingDices) == 6)
        assert(sum(keptDices) + sum(remainingDices) == 8)
        # nbKept : nbKept : the player keeps the first nbKept bits for the moment
        self.keptDices = keptDices # TODO maybe copy ?
        self.remainingDices = remainingDices

        self.is_final = True
        for i in range(6):
            if self.keptDices[i] == 0 or self.remainingDices[i] != 0:
                self.is_final = False
                # a dice can be picked, so state is not final
                break
    
    def __str__(self):
        keptDices = []
        remainingDices = []
        for dice_value in range(6):
            for j in range(self.keptDices[dice_value]):
                keptDices.append(dice_value + 1)
            for j in range(self.remainingDices[dice_value]):
                remainingDices.append(dice_value + 1)
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
        if self.keptDices[5] == 0: # player did not keep a worm : failed !
            return Rewards.C
        if self.is_final:
            return Rewards.C

        dices_sum = 0
        for dice_value in range(6):
            dices_sum += self.keptDices[dice_value] * (dice_value + 1)
        if dices_sum < 21:
            return Rewards.C
        #If sum is over the max usable sum, use it at this maximum. 
        if dices_sum > len(Rewards.R):
            dices_sum = len(Rewards.R)-1
        return Rewards.R[reward]
        

def reward(s : State, a):
    if a != Action.STOP:
        return 0 # reward is 0 for intermediate states (where player chooses to continue)
    
    return s.get_kept_value()

def compute_opt_policy(s : State):
    # first, compute reward and action (STOP) for every final state
    
    # policy = {} # maps a state to a (action, reward) pair

    # for k in range(9):
    #     for keptDices in utils.generate_distributions(k):
    #         for remainingDices in utils.generate_distributions(8 - k):

    #             s = State(keptDices, remainingDices)

    #             if s.is_final_state():
    #                 a = Action.STOP
    #                 policy[s] = (a, reward(s, a))
    
    
    print("finished !")

compute_opt_policy()