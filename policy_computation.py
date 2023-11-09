import math
import pickle
import queue
import time
from pickomino_project import *
from utils import *

def opt_policy(total_dices : int  = 8, progress_indicator : bool = False):
    probability = compute_probability(total_dices) # Generate the probability of every dices distribution.
    policy = {} # maps a state to a (action, expected_reward) pair
    
    def expected_reward(s : State, a : Action):

        
        # i = 4 # used only to compute reward for >= i pickominos
        if a.stop:
            # player wants to stop. First, we apply action a on state s and then we evaluate the reward
            if a.value == None:
                '''Reward with r vector and C'''
                return Rewards.C # LOSE
                '''Reward for >= i pickominos or Tile 24 or Tile 27'''
                # return 0
            else:
                dices = list(s.keptDices) 
                dices[a.value] = s.remainingDices[a.value] # apply action a (chose dices a.value)
                dices = tuple(dices)
                sum_dices = sum_values(dices)
                '''Reward with r vector and C'''
                if sum_dices < 21:
                    return Rewards.C
                return Rewards.R[sum_dices]
                '''Reward for >= i pickominos'''
                # if Rewards.R[sum_dices] < i:
                #     return 0
                # return 1
                '''Reward for Tile 24'''
                # return sum_dices == 24
                '''Reward for Tile >=27'''
                # return sum_dices >= 27
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

    with open("polyci_cm3.pk1", "wb") as file:
        pickle.dump(policy, file)

    remainingDices = (1, 1, 0, 3, 2, 1)
    (action, gain) = policy[State((0,0,0,0,0,0),remainingDices)]
    #pretty_print_strategy(policy)
    print("Pour le lancer", remainingDices, "La strategie optimale est de choisir l'action : ", action, " et cela apporte un gain moyen : ", gain)


def subquestions():
    policy = opt_policy(progress_indicator=True)

    # with open("policy_c0.pk1", "rb") as file: # load policy from file so that we don't re-compute it each run
    #     policy = pickle.load(file)

    probability = compute_probability(8)    

    # probas = {} # probas[s] is the probability of getting to state s in a player's turn

    # Useless BFS

    # k = 0
    # state_queue = queue.Queue()
    # initKeptDices = (0, 0, 0, 0, 0, 0)
    # for remainingDices in generate_distributions(8): # enqueue initial states
    #     initState = State(initKeptDices, remainingDices)
    #     probas[initState] = probability[remainingDices] # mark initState as visited at the same time
    #     state_queue.put(initState)
    
    # while state_queue.qsize() > 0:
    #     if len(probas) // 1000 > k:
    #         k+=1
    #         print(k)

    #     state = state_queue.get() # current state
    #     action = policy[state][0] # associated action by the policy
    #     newKeptDices = list(state.keptDices)
    #     if action.value != None:
    #         newKeptDices[action.value] = state.remainingDices[action.value] # apply action
    #     newKeptDices = tuple(newKeptDices)
    #     nRemainingDices = 8 - sum(newKeptDices) # number of remaining dices after applying action

    #     if action.stop: # we reached a final state
    #         continue

    #     for remainingDices in generate_distributions(nRemainingDices):
    #         newState = State(newKeptDices, remainingDices)
    #         if newState in probas:
    #             probas[newState] += probas[state] * probability[remainingDices]
    #         else: # newState has never been visited, enqueue it
    #             probas[newState] = probas[state] * probability[remainingDices]
    #             state_queue.put(newState)
    
    # return probas

    # computes expected reward over all initial throws
    res = 0
    initDices = (0, 0, 0, 0, 0, 0)
    for remainingDices in generate_distributions(8):
        initState = State(initDices, remainingDices)
        res += policy[initState][1] * probability[remainingDices]
    print("Reward over all initial throws is ", res)


def test():
    print("Début des tests de policy_computation.py :")
    start = time.time()
    test_opt_policy(True)
    print(f"Temps écoulé : {round(time.time() - start, 2)} secondes")
    #test_opt_policy1(True)
    print("Fin des tests de policy_computation.py")

#test()
subquestions()

# with open("policy_c0.pk1", "rb") as file:
#     policy_c0 = pickle.load(file)

# with open("policy_cm3.pk1", "rb") as file:
#     policy_cm3 = pickle.load(file)

# i = 0
# for remainingDices in generate_distributions(8):
#     s = State((0, 0, 0, 0, 0, 0), remainingDices)
#     if(policy_c0[s][0] != policy_cm3[s][0]) and policy_c0[s][1] < 1.25:
#         print(s)
#         print(policy_c0[s][0], policy_c0[s][1])
#         print(policy_cm3[s][0], policy_cm3[s][1])
#         print("----------------------------------")
#         i += 1
# print(i)