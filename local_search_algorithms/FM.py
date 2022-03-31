import numpy as np
from llist import dllist
from numba import jit
from sklearn.metrics import max_error
from local_search_algorithms.count_calls import count_calls

def FM(stopping_criterion, solution, graph):
    """
        Fiduccia-Maththyeses (FM) local search algorithm for graph bipartitioning
    
    Args:
        stopping_criterion: () -> bool 
        solution: list of bits
        graph: list of lists of int    
    Returns:
        (best_solution, min_cut): best partition of the graph found until stopping criterion is not reached
        & minimum number of cuts in this partition
    """
    
    last_solution, last_cut = FM_pass(solution, graph)    
    while not stopping_criterion():
        solution, cut = FM_pass(last_solution, graph)        
        if cut < last_cut:
            last_solution, last_cut = solution, cut
        else:
            break
        
    return last_solution, last_cut

@count_calls
def FM_pass(solution, graph):            
    """"
        Fiduccia-Maththyeses pass (FM_pass) local search algorithm for graph bipartitioning


        Complexity O(|E|) - linear in number of edges    
        ------------------------------------------------------------------------------------------------------------------------------
        Bucket data structure: Dictionary with gain as key and a doubly linked list of vertices with the corresponding gain as element
        Cells: The list of references to the vertices objects in the doubly linked list 
        (this references are kept to make the complexity of removing from list O(1))
        locked_vertices: a list that keep the order in which the vertices were chosen
        (this list is kept in order to reconstruct the best solution from the initial configuration)
        free_vertices: a list of bits that mark if a vertex is free (used when the bucket gains are updated)
        gains: a list of int with gain for each vertex (used to update buckets in O(1))
        
    Args:
        solution (list of bits)
        graph (list of ints)

    Returns:
        best_partition, minimal_cut (list of bits, int ): best partition of the graph found after a pass & minimum number of cuts in this partition
    """
    
    N = len(graph)    
    assert(N % 2 == 0)    
    initial_solution = solution[:]                   
    
    ##### initializing    
    left_bucket, right_bucket, gains, cut, cells, max_degree = compute_gain_buckets(solution, graph)                    
    cuts, locked_vertices, free_vertices = np.zeros(N+1,dtype= int), np.zeros(N,dtype= int), np.ones(N, dtype=int)     
    cuts[0] = cut
    ##### -------------    
            
    ### removing vertex with the max gain and updating buckets    
    for i in range(N):    
        # choosing the bucket with the biggest nr of vertices
        bucket = left_bucket if (i % 2 == 0) else right_bucket                                
         
        for j in range(len(bucket) - 1, -1, -1):  
            if not bucket[j].size == 0:
                best_gain = j
                break                
                    
        v_fixed = bucket[best_gain].first.value # getting the first vertex with max gain from bucket                    
        solution[v_fixed] = 1 - solution[v_fixed] ## changing sides
        locked_vertices[i] = v_fixed # lock the vertex
        free_vertices[v_fixed] = 0 # mark as non-free
        cuts[i + 1] = cuts[i] - int(best_gain - max_degree) # save cuts value                        
        bucket[best_gain].remove(cells[v_fixed]) ## remove from bucket  O(1)                                              
        
        
        # updating gains and buckets        
        for v in graph[v_fixed]: ## getting the vertices for which gain to be updated
            if free_vertices[v] == 1: ## update only if vertex is free (not locked)
                delta_gain = -2 if solution[v_fixed] == solution[v] else 2                                     
                bucket = left_bucket if (solution[v] == 0) else right_bucket                
                                
                bucket[gains[v] + max_degree].remove(cells[v])                                                                                                                    
                gains[v] += delta_gain  
                                                                    
                bucket[gains[v]  + max_degree].appendright(v)
                cells[v] = bucket[gains[v] + max_degree].last
                                    
    return find_optimal_solution(initial_solution, cuts, locked_vertices)


def compute_gain_buckets(solution, graph):
    """
        Compute initial gains, initial cut and constructing buckets
        Complexity: O(|E|) - linear in number of edges    
    """ 
    
    N = len(graph)  
    max_degree = 0
    for i in range(N):
       if len(graph[i]) > max_degree:
           max_degree = len(graph[i])
    
    left_bucket, right_bucket = [], []               
    for i in range(2*max_degree + 2):
        left_bucket.append(dllist())
        right_bucket.append(dllist())      
    
    cut = 0
    gains = np.zeros(N, dtype=int)
    cells = []
    
    for i in range(N):        
        part, vs = solution[i], graph[i]
        m = len(vs)
        co = int(np.sum(solution[vs])) ## all the ones in solution
        gain = part * (m - co) + (1 - part) * co      # if part == 0 then the counterpart with the sum of ones is co else the counterpart with sum of zeros is m - co, this is the positive part of gain
        cut += gain
        gain -= ((1 - part) * (m - co) + (part) * co) # if part == 0 then (m - co) zeros to subtract else co ones to subtract, the negative part of gain
        gain = int(gain)
        gains[i] = gain

        bucket = left_bucket if part == 0 else right_bucket                                
                                
        bucket[gain + max_degree].appendright(i)            
        cells.append(bucket[gain + max_degree].last)            
        
    return left_bucket, right_bucket, gains, int(cut/2), cells, max_degree

@jit
def find_optimal_solution(solution, cuts, locked_vertices): 
    """
        Finds the optimal solution in the FM_pass
        
    Args:
        solution (list of bits): initial solution passed in FM_pass
        cuts (list of int): the list of minimal cuts for each configuration
        locked_vertices (list of int): the order of locked vertices (used to restore configuration from initial solution)

    Returns:
        best_configuration & the cuts in this configuration
    """
    min_index = get_min_index(cuts)        
    return restore_configuration(solution, locked_vertices, min_index), cuts[min_index]

@jit
def get_min_index(cuts):    
    """
        Search for index where the cut is minimal in cuts that are valid
    """   
    min_index = 0
    for i in range(0, len(cuts), 2):          
        if cuts[i] < cuts[min_index]:
            min_index = i
    return min_index

@jit
def restore_configuration(solution, locked_vertices, min_index):
    """
        Restore configuration of the min cut from the initial solution    
    """
    for i in range(min_index):
        solution[locked_vertices[i]] = 1 - solution[locked_vertices[i]]    
    return solution