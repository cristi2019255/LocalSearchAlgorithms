from random import sample
from local_search_algorithms.FM import FM
from local_search_algorithms.utils import generate_random_solution
import numpy as np
from tqdm import tqdm

def ILS(nr_of_runs = 25, graph = []):
    N = len(graph)
    solution = generate_random_solution(N)
    optimum, min_cuts = FM(solution, graph)
    for _ in tqdm(range(nr_of_runs)):
        new_optimum, cuts = FM(mutate(optimum), graph)
        if cuts < min_cuts:
            optimum = new_optimum                    
    
    return optimum, min_cuts

def mutate(solution, probability = 0.1):
    N = len(solution)    
    zeros = []
    ones = []
    probabilities = np.random.random(N) <= probability 
    for i in range(N):
        if probabilities[i] == 1:
            solution[i] = 1 - solution[i]        
        if solution[i] == 0:
            zeros.append(i)
        else:
            ones.append(i)
    
    ## TODO: to ensure that mutated solutions are still valid 
    
    if (len(zeros) == len(ones)):
        return solution                        
    
    diff = int(abs(len(zeros) - len(ones)) / 2)
    c = sample(ones, k=diff)  if (len(zeros) < len(ones)) else sample(zeros, k=diff)
    
    for i in c:
        solution[i] = 1 - solution[i]     
    
    #print(solution)   
    #print(np.sum(solution) == int(N/2))
    return solution