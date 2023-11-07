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
            for action in action_list: #TODO
                pass #TODO    
    
    print("finished !")
    return policy

opt_policy()