from math import ceil, floor
from random import sample
from local_search_algorithms.FM import FM, FM_pass
from local_search_algorithms.utils import generate_random_solution
import numpy as np

def ILS(stopping_criterion, graph = [], probability = 0.1):
    """
    Iterated local search for graph bipartitioning problem.

    Args:
        stopping_criterion (() -> bool): the stopping criterion of the algorithm 
        graph (list, optional): Defaults to [].
        probability(float, optional): The perturbation size for solutions. Defaults to 0.1. 
    Returns:
        (list, int, float): best solution found & minimum number of cuts, same region of attraction ratio
    """
    N = len(graph)
    solution = generate_random_solution(N)
    FM_pass.set_count_calls(0) ## setting count calls of FM_pass to 0
    optimum, min_cuts = FM(stopping_criterion, solution, graph)    
    same_attraction_region = 0
    nr_perturbations = 0
    while not stopping_criterion():
        new_optimum, cuts = FM(stopping_criterion, mutate(optimum, probability = probability), graph)
        if cuts < min_cuts:
            optimum = new_optimum          
            min_cuts = cuts          
            print(f'New best optimum: {cuts}')
   
        elif cuts == min_cuts:
           same_attraction_region += 1     
        
        nr_perturbations += 1
    
    print(f'Same region of attraction: {same_attraction_region}/{nr_perturbations}')    
   
    FM_pass.set_count_calls(0) ## setting count calls of FM_pass to 0            
    return optimum, min_cuts, (same_attraction_region / nr_perturbations)

def adaptive_ILS(stopping_criterion, graph = [], P_min = 0.1, alpha = 0.5, beta = 0.5, operators = [], reward_binary = True):
    """
    Adaptive algorithm for iterated local search that choose the best perturbation operator from a list of given operators 
    for graph bipartitioning problem.

    Args:
        stopping_criterion (() -> bool): the stopping criterion of the algorithm 
        graph (list, optional): Defaults to [].
        P_min (float, optional): The minimum probability with which an operator can be applied. Defaults to 0.1.
        alpha (float, optional): Learning rate for reward estimates. Defaults to 0.5.
        beta (float, optional): Learning rate for operator probabilities estimates. Defaults to 0.5.
        operators (list, optional): The list of operators from where the algorithm is aimed to favor the best. Defaults to [].

    Returns:
        (list, int): best solution found & minimum number of cuts
    """
    N = len(graph)
    K = len(operators)
    P_max = 1 - (K-1) * P_min 
    operators_probabilities = [1/K] * K
    estimated_rewards = [1.0] * K
    
    solution = generate_random_solution(N)
    optimum, min_cuts = FM(stopping_criterion, solution, graph)        
        
    FM_pass.set_count_calls(0) ## setting count calls of FM_pass to 0                
    while not stopping_criterion():
        operator_index = np.random.choice(range(K), 1, p=operators_probabilities)[0]        
        operator_selected = operators[operator_index]
        new_optimum, cuts = FM(stopping_criterion, mutate(optimum, probability = operator_selected), graph)
        if cuts < min_cuts:
            optimum = new_optimum          
            min_cuts = cuts          
            reward = 1 if reward_binary else (min_cuts - cuts)
            print(f'New best optimum: {cuts}')
        else:
            reward = 0
        
        estimated_rewards[operator_index] += alpha * (reward - estimated_rewards[operator_index])
        best_operator_index = np.argmax(estimated_rewards)        
        for i in range(K):
            if i == best_operator_index:
                operators_probabilities[best_operator_index] += beta * (P_max - operators_probabilities[best_operator_index])
            else:
                operators_probabilities[i] += beta * (P_min - operators_probabilities[i])

    print(operators_probabilities)
    FM_pass.set_count_calls(0) ## setting count calls of FM_pass to 0            
    return optimum, min_cuts

def mutate(solution, probability = 0.1):
    """ Mutates a solution by randomly choosing a subset of vertices and flipping their labels.

    Args:
        solution (list): list of bits representing a solution for graph bipartitioning problem.
        probability (float, optional): perturbation size. Defaults to 0.1.

    Returns:
        list: the mutated solution
    """
    N = len(solution) 
    zeros_indexes, ones_indexes = [], []    
    for i in range(N):
        if solution[i] == 1:
            ones_indexes.append(i)        
        else:
            zeros_indexes.append(i)
        
        
    p = probability * N/2           
    k = int(ceil(p)) if p % 1 > np.random.random() else int(floor(p))        
        
    ones_indexes_chosen = sample(ones_indexes, k=k) 
    zeros_indexes_chosen = sample(zeros_indexes, k=k)     
    
    for i in range(k):        
        solution[ones_indexes_chosen[i]] = 0    
        solution[zeros_indexes_chosen[i]] = 1
    
    return solution   