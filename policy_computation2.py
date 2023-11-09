import math
import time
import pickle
from pickomino_project2 import *
from utils import *

def opt_policy(rewards : Rewards, total_dices : int  = 8,  progress_indicator : bool = False):
    probability = compute_probability(total_dices) # Generate the probability of every dices distribution.
    policy = {} # maps a state to a (action, expected_reward) pair

    def expected_reward(s : State, a : Action):
        if a.stop:
            #Player wants to stop. First, we apply action a on state s and then we evaluate the reward
            if a.value == None:
                return rewards.get_reward(0)[1] # LOSE
            else:
                dices = list(s.keptDices) # TODO is these 3 lines a performance bottleneck ??
                dices[a.value] = s.remainingDices[a.value] # apply action a (chose dices a.value)
                dices = tuple(dices)
                return rewards.get_reward(sum_values(dices))[1]
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

def simulate_game(dices, dominos, alpha_player, beta_player, alpha_opponent, beta_opponent):
    opponent_dominos = []
    player_dominos = []
    board_dominos = dominos
    
    #We save the already computed policies to avoid many time loss
    try:
        file = open("policy_c0.pk1", "rb")
        policies = pickle.load(file)
        file.close()
    except:
        policies = {}

    def get_policy(alpha, beta, player_domino, opponent_domino):
        key = (alpha, beta, player_domino, opponent_domino)
        if not (key in policies.keys()):
            rewards = Rewards(board_dominos, player_domino, opponent_domino, alpha, beta)
            policy = opt_policy(rewards,total_dices = dices)
            policies[key] = policy
        return policies[key]

    def best_domino(board_dominos):
        best = board_dominos[0]
        for domino in board_dominos:
            if best[1]<domino[1]:
                best = domino
        return best

    def simulate_round(policy, rewards, player_dominos, opponent_dominos):
        keptDices = (0,0,0,0,0,0)
        remainingDices = throw(8)
        action = policy[State(keptDices,remainingDices)][0]
        while not action.stop:
            keptDices = list(keptDices)
            keptDices[action.value] = remainingDices[action.value]
            keptDices = tuple(keptDices)

            remainingDices = throw(dices - sum(keptDices))
            action = policy[State(keptDices,remainingDices)][0]
        #The player has ended its turn, it is now time to face the consequences:
        if action.value==None:
            value=0
        else:
            keptDices = list(keptDices)
            keptDices[action.value] = remainingDices[action.value]
            keptDices = tuple(keptDices)
            value = sum_values(keptDices)
        
        domino = rewards.get_reward(value)[0]
        if domino == None:
            print("Loses")
            #Case where no domino is taken
            board_dominos.remove(best_domino(board_dominos))
            if len(player_dominos)>0:
                board_dominos.append(player_dominos.pop())
        elif (len(opponent_dominos)>0 and domino == opponent_dominos[-1]):
            print("Steals ", domino)
            #Case where the player steals its opponent
            player_dominos.append(opponent_dominos.pop())
        else:
            print("Takes", domino)
            #Case where the player simply take a domino from board
            player_dominos.append(domino)
            board_dominos.remove(domino)

    while board_dominos != []:
        if len(player_dominos)>0:
            player_domino = player_dominos[-1]
        else:
            player_domino = None
        if len(opponent_dominos)>0:
            opponent_domino = opponent_dominos[-1]
        else:
            opponent_domino = None
        policy = get_policy(alpha_player, beta_player, player_domino, opponent_domino)
        rewards = Rewards(board_dominos, player_domino, opponent_domino, alpha_player, beta_player)
        print("Player :")
        simulate_round(policy, rewards, player_dominos, opponent_dominos)
        
        if board_dominos !=[]:
            #And now the opponent round
            if len(player_dominos)>0:
                player_domino = player_dominos[-1]
            else:
                player_domino = None
            if len(opponent_dominos)>0:
                opponent_domino = opponent_dominos[-1]
            else:
                opponent_domino = None
            policy = get_policy(alpha_opponent, beta_opponent, opponent_domino, player_domino)
            rewards = Rewards(board_dominos, opponent_domino, player_domino, alpha_opponent, beta_opponent)
            print("Opponent :")
            simulate_round(policy, rewards, opponent_dominos, player_dominos)
    
    player_score = 0
    for domino in player_dominos:
        player_score += domino[1]
    opponent_score = 0
    for domino in opponent_dominos:
        opponent_score += domino[1]
    with open("policy_c0.pk1", "wb+") as file:
        pickle.dump(policies,file)
    return (player_score, opponent_score)

###############
#### TESTS ####
###############

def test_simulate_game():
    print(simulate_game(8, [(21,1),(22,1),(23,1),(24,1),(25,2),(26,2),(27,2),(28,2),(29,3),(30,3),(31,3),(32,3),(33,4),(34,4),(35,4),(36,4)], 1, 1, 1, 1))

def test_opt_policy(progress_indicator):
    rewards = Rewards([(21,1),(22,1),(23,1),(24,1),(25,2),(26,2),(27,2),(28,2),(29,3),(30,3),(31,3),(32,3),(33,4),(34,4),(35,4),(36,4)], None, None, 1, 1)
    policy = opt_policy(rewards, progress_indicator=progress_indicator)
    (action, gain) = policy[State((0,0,0,0,0,0),(1, 1, 0, 3, 2, 1))]
    #pretty_print_strategy(policy)
    print("La strategie optimale est de choisir l'action : ", action, " et cela apporte un gain moyen : ", gain)

def test():
    print("Début des tests de policy_computation.py :")
    start = time.time()
    #test_opt_policy(True)
    test_simulate_game()
    print(f"Temps écoulé : {round(time.time() - start, 2)} secondes")
    #test_opt_policy1(True)
    print("Fin des tests de policy_computation.py")

test()