def generate_distributions(number_dices : int):
    '''Return a list of all the distribution one can get by throwing number_dices dices'''
    res = []
    for x1 in range(0, number_dices+1):
        for x2 in range(0, number_dices+1 -x1):
            for x3 in range(0, number_dices+1 -x1 -x2):
                for x4 in range(0, number_dices+1 -x1 -x2 -x3):
                    for x5 in range(0, number_dices+1 -x1 -x2 -x3 -x4):
                        x6 = number_dices -x1 -x2 -x3 -x4 -x5
                        res.append((x1,x2,x3,x4,x5,x6))
    return res
    
def compute_probability(max_dices : int):
    '''Return a hash table that associates to a distribution (x1, x2, x3, x4, x5, x6)
    the probability to get such a distribution by throwing x1+x2+x3+x4+x5+x6 dices.
    All the distribution that throw max_dices or less dices are included.'''
    probability = {}
    #Initialisation for the 1 dice
    probability[(0,0,0,0,0,0)] = 1
    #Initialisation for the 1 dice
    for n in range(1,max_dices+1):
        for distribution in generate_distributions(n):
            p = 0
            for value in range(6):
                if distribution[value] > 0:
                    previous_distribution = list(distribution)
                    previous_distribution[value] -= 1
                    previous_distribution = tuple(previous_distribution)
                    p += 1/6 * probability[previous_distribution]
            probability[distribution] = p
    return probability

def sum_values(dices):
    '''Compute the value of a dice set'''
    res = 5 * dices[0]
    for dice_value in range(1, 6):
        res += dices[dice_value] * dice_value
    return res

###############
#### TESTS ####
###############

def test_compute_probability():
    probability = compute_probability(8)
    sum = 0
    for distribution in generate_distributions(8):
        sum += probability[distribution]
    print("La somme des probabilité d'apparition de chaque jeté de 8 dés est ",sum)
          
def run_tests():
    print("Début des tests :")
    test_compute_probability()

run_tests()