import math
from pickomino_project import *
from utils import *

def opt_policy():
    policy = {} # maps a state to a (action, expected_reward) pair

    def expected_reward(s, a):
        if a == 0:
            pass
    

    def opt_policy_state(s):
        if s in policy:
            return policy[s]
        else:
            max_expected = -math.inf
            best_action = None
            for action in s.possibleActions:
                if expected_reward(s, a):
                    pass


    
    #for k in range(9):
    #    for keptDices in generate_distributions(k):
    #        for remainingDices in generate_distributions(8 - k):
    #            s = State(keptDices, remainingDices)
    #            if s.is_final_state():
    #                a = Action.STOP
    #                policy[s] = (a, reward(s, a))
    
    
    print("finished !")
    return policy

opt_policy()