from local_search_algorithms.FM import FM
from local_search_algorithms.utils import generate_random_solution

def MLS(nr_of_runs = 1000, graph = []):
    N = len(graph)
    assert(N % 2 == 0)
    min_cuts, best_optimum = N, None    
    for _ in range(nr_of_runs):
        solution = generate_random_solution(N)
        local_optimum, cuts = FM(solution, graph)
        
        if cuts < min_cuts:
            best_optimum = local_optimum
            min_cuts = cuts
                
    return best_optimum, min_cuts