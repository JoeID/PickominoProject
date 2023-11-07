import utils

class Rewards:
    C = 0
    R = [0 for i in range(21)] + [1 + i // 4 for i in range(16)]


class Action:
    STOP = 0


class State:

    def __init__(self, keptDice, remainingDice):
        # keptDice : list of length 6 that indicates how many dice i the player has kept
        # remainingDice : similar
        assert(len(keptDice) == 6 and len(remainingDice) == 6)
        assert(sum(keptDice) + sum(remainingDice) == 8)
        # nbKept : nbKept : the player keeps the first nbKept bits for the moment
        self.keptDice = keptDice # TODO maybe copy ?
        self.remainingDice = remainingDice

        self.is_final = True
        for i in range(6):
            if self.keptDice[i] == 0 or self.remainingDice[i] != 0:
                self.is_final = False
                # a dice can be picked, so state is not final
                break
    
    def __str__(self):
        keptDice = []
        remainingDice = []
        for dice_value in range(6):
            for j in range(self.keptDice[dice_value]):
                keptDice.append(dice_value + 1)
            for j in range(self.remainingDice[dice_value]):
                remainingDice.append(dice_value + 1)
        return "Kept dice : " + str(keptDice) + " Remaining dice " + str(remainingDice)
            
    def is_final(self):
        # returns true iff state is final ; that is no dice can be picked
        # the boolean value is_final is computed at init for performance reasons
        return self.is_final

    def get_kept_value(self):
        # assuming player chooses to stop immediately, how many points do they have ?
        if self.keptDice[5] == 0: # player did not keep a worm : failed !
            return Rewards.C
        if self.is_final:
            return Rewards.C

        reward = 0
        for dice_value in range(6):
            reward += self.keptDice[dice_value] * (dice_value + 1)
        if reward < 21:
            return Rewards.C
        
        return Rewards.R[reward]
        

def reward(s : State, a):
    if a != Action.STOP:
        return 0 # reward is 0 for intermediate states (where player chooses to continue)
    
    return s.get_kept_value()

def enumerate_lists(total, length):
    if length == 1:
        yield [total]
    else:
        for i in range(total + 1):
            for l in enumerate_lists(total - i, length - 1):
                l.append(i)
                yield l


i = 0
for l in enumerate_lists(8, 12):
    i += 1
print(i)