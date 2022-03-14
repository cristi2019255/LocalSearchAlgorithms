from random import sample
from local_search_algorithms.FM import FM, FM_pass
from local_search_algorithms.utils import generate_random_solution
import numpy as np

def ILS(nr_of_calls = 25, graph = [], probability = 0.1):
    N = len(graph)
    solution = generate_random_solution(N)
    FM_pass.set_count_calls(0) ## setting count calls of FM_pass to 0
    optimum, min_cuts = FM(solution, graph)    
    
    while(FM_pass.call_count <= nr_of_calls):
        new_optimum, cuts = FM(mutate(optimum, probability = probability), graph)
        if cuts < min_cuts:
            optimum = new_optimum          
            min_cuts = cuts          
            print(f'New best optimum: {cuts}')

    FM_pass.set_count_calls(0) ## setting count calls of FM_pass to 0            
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
    
    ## Ensuring that mutated solutions are still valid 
    
    if (len(zeros) == len(ones)):
        return solution                        
    
    diff = int(abs(len(zeros) - len(ones)) / 2)
    c = sample(ones, k=diff)  if (len(zeros) < len(ones)) else sample(zeros, k=diff)
    
    for i in c:
        solution[i] = 1 - solution[i]     
    
    #print(solution)   
    #print(np.sum(solution) == int(N/2))
    return solution