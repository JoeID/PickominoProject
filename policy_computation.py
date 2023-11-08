import math
import time
from pickomino_project import *
from utils import *

def opt_policy(total_dices : int  = 8, progress_indicator : bool = False):
    probability = compute_probability(total_dices) # Generate the probability of every dices distribution.
    policy = {} # maps a state to a (action, expected_reward) pair
    
    def expected_reward(s : State, a : Action):

        if a.stop:
            # player wants to stop. First, we apply action a on state s and then we evaluate the reward
            if a.value == None:
                return Rewards.C # LOSE
            else:
                dices = list(s.keptDices) # TODO is these 3 lines a performance bottleneck ??
                dices[a.value] = s.remainingDices[a.value] # apply action a (chose dices a.value)
                dices = tuple(dices)
                return Rewards.R[sum_values(dices)]
        else:
            new_keptDices = list(s.keptDices)
            new_keptDices[a.value] = s.remainingDices[a.value] # apply action a (chose dices a.value)
            new_keptDices = tuple(new_keptDices)
            number_dices = total_dices - sum(new_keptDices)
            res = 0
            for remainingDices in generate_distributions(number_dices): # for every possible roll of remaining dices
                reward = opt_policy_state(State(new_keptDices,remainingDices))[1]
                res += reward * probability[remainingDices]
            return res
    
    def opt_policy_state(s : State):   
        # returns best action and associated expected reward from state s     

        if not s in policy:

            if progress_indicator :
                if len(policy)%1000==0:
                    print(len(policy), s)

            max_expected = -math.inf
            best_action = None

            for a in s.get_possibleActions(): # for every possible next action
                a_reward = expected_reward(s, a)
                if a_reward>max_expected:
                    max_expected = a_reward
                    best_action = a
            policy[s] = (best_action, max_expected)
        return policy[s]

    #Computing the optimal policy for all possible starting state
    for remainingDices in generate_distributions(total_dices):
        s = State((0,0,0,0,0,0), remainingDices)
        opt_policy_state(s)
    if progress_indicator:
        print("Optimal policy computed.")
    return policy


###############
#### TESTS ####
###############
def test_opt_policy1(progress_indicator):
    policy = opt_policy(progress_indicator=progress_indicator)
    little_policy = {}
    for key in policy:
        if sum(key.remainingDices)==1:
            little_policy[key] = policy[key]
    pretty_print_strategy(little_policy)

def test_opt_policy(progress_indicator):
    policy = opt_policy(progress_indicator=progress_indicator)
    (action, gain) = policy[State((0,0,0,0,0,0),(1, 1, 0, 3, 2, 1))]
    #pretty_print_strategy(policy)
    print("La strategie optimale est de choisir l'action : ", action, " et cela apporte un gain moyen : ", gain)

def test():
    print("Début des tests de policy_computation.py :")
    start = time.time()
    test_opt_policy(True)
    print(f"Temps écoulé : {round(time.time() - start, 2)} secondes")
    #test_opt_policy1(True)
    print("Fin des tests de policy_computation.py")

test()