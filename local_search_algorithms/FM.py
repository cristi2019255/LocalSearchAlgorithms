import numpy as np

def FM(solution, graph):
    "Fiduccia-Maththyeses (FM) local search algorithm for graph bipartitioning"
    
    N = len(graph)
    fixed_vertices = np.zeros(N)
    
    ### hardcoded just for testing
    cuts = 5

    
    return solution, cuts