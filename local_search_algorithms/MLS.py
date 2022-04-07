from local_search_algorithms.FM import FM, FM_pass
from local_search_algorithms.utils import generate_random_solution

def MLS(stopping_criterion, graph = []):
    N = len(graph)
    assert(N % 2 == 0)
    min_cuts, best_optimum = N * N, None    
    
    FM_pass.set_count_calls(0) ## setting the number of calls of FM_pass to 0    
    
    while not stopping_criterion():
        solution = generate_random_solution(N)
        local_optimum, cuts = FM(stopping_criterion, solution, graph)
        
        if cuts < min_cuts:
            print("New best optimum: " + str(cuts))
            best_optimum = local_optimum
            min_cuts = cuts
    print(FM_pass.call_count)
    FM_pass.set_count_calls(0) ## setting the number of calls of FM_pass to 0
    return best_optimum, min_cuts