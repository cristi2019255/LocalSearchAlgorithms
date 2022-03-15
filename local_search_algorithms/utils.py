import numpy as np

def generate_random_solution(N):
    """ Generating a random solution for graph bipartitioning

    Args:
        N (int): the length of solution

    Returns:
        list: the generated random solution
    """
    positions = np.random.choice(N, int(N/2), replace=False)        
    solution = np.zeros(N)
    for i in positions:
        solution[i] = 1
    return solution