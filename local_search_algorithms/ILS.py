from local_search_algorithms.FM import FM
from local_search_algorithms.utils import generate_random_solution
import numpy as np

def ILS(nr_of_runs = 25, graph = []):
    N = len(graph)
    solution = generate_random_solution(N)
    optimum, min_cuts = FM(solution, graph)
    for _ in range(nr_of_runs):
        new_optimum, cuts = FM(mutate(optimum), graph)
        if cuts < min_cuts:
            optimum = new_optimum                    
    
    return optimum, min_cuts

def mutate(solution, probability = 0.1):
    probabilities = np.random.random(len(solution)) <= probability 
    for i in range(len(solution)):
        if probabilities[i] == 1:
            solution[i] = 1 - solution[i]        
    ## to ensure that mutated solutions are still valid 
    ## for now not implemented
    return solution