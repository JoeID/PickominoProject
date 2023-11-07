from pickomino_project import *
from utils import *

def opt_policy(s : State):
    # first, compute reward and action (STOP) for every final state
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

    
    #for k in range(9):
    #    for keptDices in generate_distributions(k):
    #        for remainingDices in generate_distributions(8 - k):
    #            s = State(keptDices, remainingDices)
    #            if s.is_final_state():
    #                a = Action.STOP
    #                policy[s] = (a, reward(s, a))
    
    
    print("finished !")

opt_policy()