import numpy as np
import math

def generate_graph(size = 10, fully_connected = False, random = False):    
    """ Generate a graph for graph bipartitioning problem

    Args:
        size (int, optional): The number of vertices for the generated graph. Defaults to 10.
        fully_connected (bool, optional): If is set to True the generated graph is fully connected. Defaults to False.
        random (bool, optional): If set to True each vertex 'i' in the generated graph besides edges to vertices 'i-1' and 'i+1'
        has edges to 3 random chosen vertices. Defaults to False.

    Returns:
        list of lists, list: the generated graph, vertices positions in plane
    """
    graph = []
    pos = []    
    dtheata = 2* math.pi/size
    theta = 0
    x = np.cos(theta) + 0.5
    y = np.sin(theta) + 0.5
    if fully_connected:
        for i in range(size):                        
            graph.append(list(np.append(np.arange(i), np.arange(i+1, size))))
            pos.append((x,y))            
            theta += dtheata
            x = np.cos(theta) + 0.5
            y = np.sin(theta) + 0.5 
            
    else:
        for i in range(size):
            if i == size - 1:
                graph.append([i-1,0])
                pos.append((x,y))
            else:           
                if i == 0:
                    graph.append([size - 1,i+1])        
                    pos.append((x,y))                
                else: 
                    graph.append([i-1,i+1])                       
                    pos.append((x,y)) 
            
            theta += dtheata
            x = np.cos(theta) + 0.5
            y = np.sin(theta) + 0.5 
        if random:
            for i in range(size):
                if i < size - 1:
                    nr = 3#np.random.randint(0, high=size)
                    vs = np.random.randint(0 , high = size, size = nr)                     
                    for v in vs:
                        if not (v == i):
                            if not (v in graph[i]):
                                graph[i].append(v)
                            if not (i in graph[v]):
                                graph[v].append(i)
    return graph, pos

def save_graph(file_name, graph, pos):
    """ Saving the graph to a file
    """
    with open(file_name,'w') as f:
        for i in range(len(graph)):
            line = str((i+1)) + ' ' + '(' + str(pos[i][0]) + ',' + str(pos[i][1]) + str(len(graph[i]))
            for v in graph[i]:
                line += ' ' + str(v + 1)
            line += '\n'
            f.write(line)
        f.close()    
 