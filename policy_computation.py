import math
from pickomino_project import *
from utils import *

def opt_policy(progress_indicator = False):
    probability = compute_probability(8) #Generate the probability of every dices distribution.
    policy = {} # maps a state to a (action, expected_reward) pair
    deja_vu = set()

    def expected_reward(s : State, a : Action):
        if a.stop:
            if a.value == None:
                return Rewards.C
            else:
                dices = list(s.keptDices)
                dices[a.value] = s.remainingDices[a.value]
                dices = tuple(dices)
                return Rewards.R[sum_values(dices)]
        else:
            new_keptDices = list(s.keptDices)
            new_keptDices[a.value] = s.remainingDices[a.value]
            new_keptDices = tuple(new_keptDices)
            number_dices = 8 - sum(new_keptDices)
            res = 0
            for remainingDices in generate_distributions(number_dices):
                reward = opt_policy_state(State(new_keptDices,remainingDices))[1]
                res += reward * probability[remainingDices]
            return res
    
    def opt_policy_state(s : State):        
        if not s in policy:
            if progress_indicator :
                if len(policy)%1000==0:
                    print(len(policy), s)
            max_expected = -math.inf
            best_action = None
            for a in s.get_possibleActions():
                a_reward = expected_reward(s, a)
                if a_reward>max_expected:
                    max_expected = a_reward
                    best_action = a
            policy[s] = (best_action, max_expected)
        return policy[s]

    #Computing the optimal policy for all possible starting state
    for remainingDices in generate_distributions(8):
        s = State((0,0,0,0,0,0), remainingDices)
        opt_policy_state(s)
    if progress_indicator:
        print("Optimal policy computed.")
    return policy


###############
#### TESTS ####
###############
def test_opt_policy(progress_indicator):
    (action, gain) = opt_policy(True)[State((0,0,0,0,0,0),(1, 1, 0, 3, 2, 1))]
    print(action, gain)

def test():
    test_opt_policy(True)
test()