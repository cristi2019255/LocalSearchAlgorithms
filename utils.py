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
