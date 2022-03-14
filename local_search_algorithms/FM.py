import numpy as np
from llist import dllist
from numba import jit
from local_search_algorithms.count_calls import count_calls

def FM(solution, graph):
    "Fiduccia-Maththyeses (FM) local search algorithm for graph bipartitioning"
    
    last_solution, last_cut = FM_pass(solution, graph)    
    while True:
        solution, cut = FM_pass(last_solution, graph)        
        if cut < last_cut:
            last_solution, last_cut = solution, cut
        else:
            break
                
    #print("solution: " + str(last_solution))
    #print("min cuts: " + str(last_cut))
    return last_solution, last_cut

@count_calls
def FM_pass(solution, graph):            
    N = len(graph)    
    assert(N % 2 == 0)    
    initial_solution = solution[:]                   
    
    ##### initializing    
    left_bucket, right_bucket, gains, cut, cells = compute_gain_buckets(solution, graph)                    
    cuts, locked_vertices, free_vertices = np.zeros(N+1,dtype= int), np.zeros(N,dtype= int), np.ones(N, dtype=int)     
    cuts[0] = cut
    ##### -------------    
    
    ### FM main idea    
    for i in range(N):    
        # choosing the bucket with the biggest nr of vertices
        bucket = left_bucket if (i % 2 == 0) else right_bucket                
            
        best_gain = max(bucket.keys())  ## O(max_degree) max_degree <= |V|               
                    
        v_fixed = bucket[best_gain].first.value # getting the first vertex with max gain from bucket                    
        solution[v_fixed] = 1 - solution[v_fixed] ## changing sides
        locked_vertices[i] = v_fixed # lock the vertex
        free_vertices[v_fixed] = 0 # mark as non-free
        cuts[i + 1] = cuts[i] - int(best_gain) # save cuts value                        
        bucket[best_gain].remove(cells[v_fixed]) ## remove from bucket                        
        
        if bucket[best_gain].size == 0:
            bucket.pop(best_gain)
        
        # updating gains and buckets        
        for v in graph[v_fixed]: ## getting the vertices for which gain to be updated
            if free_vertices[v] == 1: ## update only if vertex is free (not locked)
                delta_gain = -2 if solution[v_fixed] == solution[v] else 2                                     
                bucket = left_bucket if (solution[v] == 0) else right_bucket                
                                
                bucket[gains[v]].remove(cells[v])                                                                
                
                if bucket[gains[v]].size == 0:
                    bucket.pop(gains[v]) # O(1)
                    
                gains[v] += delta_gain  
                
                if not (gains[v] in bucket.keys()): # O(1)
                    bucket[gains[v]] = dllist()
                    
                bucket[gains[v]].appendright(v)
                cells[v] = bucket[gains[v]].last
                        
    ### Complexity O(|E|) - linear in number of edges    
    ### -------------------------------------            
    return find_optimal_solution(initial_solution, cuts, locked_vertices)


def compute_gain_buckets(solution, graph):
    """
        compute initial gains, initial cut and constructing buckets
    """ 
           
    N = len(graph)    
    left_bucket, right_bucket = {},{}
    
    cut = 0
    gains = np.zeros(N, dtype=int)
    cells = []
    
    for i in range(N):        
        part = solution[i]
        vs = graph[i]
        m = len(vs)
        co = int(np.sum(solution[vs])) ## all the ones in solution O(|V|)
        gain = part * (m - co) + (1 - part) * co      # if part == 0 then the counterpart with the sum of ones is co else the counterpart with sum of zeros is m - co, this is the positive part of gain
        cut += gain 
        gain -= ((1 - part) * (m - co) + (part) * co) # if part == 0 then (m - co) zeros to subtract else co ones to subtract, the negative part of gain
        gains[i] = gain

        bucket = left_bucket if part == 0 else right_bucket                                
        
        if not (gain in bucket.keys()): #O(1)
            bucket[gain] = dllist()
        bucket[gain].appendright(i)            
        cells.append(bucket[gain].last)            
        
    ### Complexity O(|E|) - linear in number of edges    
    ### -------------------------------------        
    return left_bucket, right_bucket, gains, int(cut/2), cells

@jit
def find_optimal_solution(solution, cuts, locked_vertices): 
    min_index = get_min_index(cuts)        
    return restore_configuration(solution, locked_vertices, min_index), cuts[min_index]

@jit
def get_min_index(cuts):    
    # search for min_index in cuts that are valid
    min_index = 0
    for i in range(0, len(cuts), 2):          
        if cuts[i] < cuts[min_index]:
            min_index = i
    return min_index

@jit
def restore_configuration(solution, locked_vertices, min_index):
    # restore configuration of the min cut from the initial solution    
    for i in range(min_index):
        solution[locked_vertices[i]] = 1 - solution[locked_vertices[i]]    
    return solution