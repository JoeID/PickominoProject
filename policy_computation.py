from pickomino_project import *
from utils import *

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