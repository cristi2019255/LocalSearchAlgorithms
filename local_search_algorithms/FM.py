from copy import copy
import numpy as np

from llist import dllist

def FM_pass(solution, graph, max_degree):
    "Fiduccia-Maththyeses (FM) local search algorithm for graph bipartitioning"
    
    #solution = np.asarray([0, 0, 1, 0, 1, 1])    
    #print(solution)
    
    N = len(graph)    
    assert(N % 2 == 0)    
    
    cuts = []        
    locked_vertices = [] 
    
    
    ##### initializing the buckets
    left_bucket = {i:[] for i in range(-max_degree, max_degree + 1)} # change [] to dllist in future to optimize
    right_bucket = {i:[] for i in range(-max_degree,max_degree + 1)}
    
    cut = 0
    gains = np.zeros(N)    
    
    for i in range(len(graph)):
        vs = graph[i]
        part = solution[i]
        gain = 0        
        for v in vs:
            if part == solution[v - 1]:
                gain -= 1
            else:
                cut += 1
                gain += 1    
        if part == 0:
            left_bucket[gain].append((i + 1))
        else:
            right_bucket[gain].append((i + 1))

        gains[i] = gain
        
    cuts.append(int(cut/2))
    ##### -------------
    #print('initial buckets')
    #print(left_bucket)
    #print(right_bucket)    
    
    ### FM main idea    
    while len(locked_vertices) < N:                
        # choosing the bucket with the biggest nr of vertices
        if np.sum(solution) < int(N/2):
            bucket = left_bucket            
        else:            
            bucket = right_bucket            
            
        best_gain = max_degree 
        while best_gain >= -max_degree and len(bucket[best_gain]) == 0:
            best_gain -= 1            
            
        v_fixed = bucket[best_gain][0] # getting the first vertex with max gain from bucket
        solution[v_fixed - 1] = 1 - solution[v_fixed - 1] ## changing sides
        locked_vertices.append(v_fixed) # lock the vertex
        cuts.append( cuts[-1] - best_gain ) # save cuts value
        
        bucket[best_gain].remove(v_fixed) ## remove from bucket        
        
        # updating gains and buckets
        vs = graph[v_fixed - 1] ## getting the vertices for which gain to be updated
        for v in vs:
            if not (v in locked_vertices):  
                
                delta_gain = calculate_gain(v, solution, graph)   ## to optimize it in order not to use calculate_gain but calculate_delta_gain
                
                if (solution[v-1] == 0):
                    left_bucket[gains[v-1]].remove(v)                        
                    gains[v-1] = delta_gain
                    left_bucket[gains[v-1]].append(v)
                else:
                    right_bucket[gains[v-1]].remove(v)                        
                    gains[v-1] = delta_gain
                    right_bucket[gains[v-1]].append(v)                        

        #print('updated buckets:')
        #print(left_bucket)
        #print(right_bucket)      
        
    #print('locked_vertices' + str(locked_vertices))
    #print('cuts' + str(cuts))    
    ### rolling back to find the best solution      
    
    min_index = 0
    for i in range(0, len(cuts),2):          
        if cuts[i] < cuts[min_index]:
            min_index = i
            
    # switching back to initial solution (thought it was more easier)            
    for sol in solution:
        sol = 1 - sol
    
    for i in range(min_index):
        solution[locked_vertices[i] - 1] = 1 - solution[locked_vertices[i] - 1]
            
    return solution, cuts[i]

def calculate_gain(vertex,solution,graph):
    part = solution[vertex - 1]
    gain = 0
    vs = graph[vertex - 1]
    for v in vs:
        if part == solution[v - 1]:
            gain -= 1
        else:                
            gain += 1
    return gain

def FM(solution, graph, max_degree):
    last_solution, last_cut = FM_pass(solution, graph, max_degree)    
    while True:
        solution, cut = FM_pass(last_solution, graph, max_degree)        
        if cut < last_cut:
            last_solution, last_cut = solution, cut
        else:
            break
    
    print("solution: " + str(last_solution))
    print("min cuts: " + str(last_cut))
    return last_solution, last_cut