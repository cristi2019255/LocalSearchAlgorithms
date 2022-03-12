import math
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def read_graph_from_file(filename = ''):
    """_summary_: Reading a graph from file

    Args:
        filename (_type_, optional): _description_. Defaults to FILE_NAME.

    Returns:
        _type_: _description_
    """
    try:
        graph = []
        positions = []
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(' ')                
                x, y = data[1][1:-1].split(',')
                x, y = float(x), float(y)
                positions.append((x,y))
                vertices = data[3:]
                vertices = list(map(lambda x: x-1,list(map(int, vertices))))
                graph.append(vertices)                                
    except Exception as e:
        print(e)       
    return graph, positions

def construct_graph_nx(graph):
    G = nx.Graph()    
    for i in range(len(graph)):                     
        for v in graph[i]:
            G.add_edge(i, v)        
    return G

def plot_graph(graph, positions):
    """_summary_: visualize a graph

    Args:
        graph (_type_): _description_
    """
    G = construct_graph_nx(graph)
    nx.draw(G, with_labels = True, pos = positions)        
    plt.show()
    

def plot_partitioned_graph(graph, partition, positions):    
    color_map = []
    G = construct_graph_nx(graph)    
    for node in G:
        if partition[node] == 0:
            color_map.append('red')
        else:
            color_map.append('blue')
                    
    nx.draw(G, node_color=color_map, with_labels=True, pos=positions)
    plt.show()

def generate_graph(size = 10, fully_connected = False, random = False):    
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
    