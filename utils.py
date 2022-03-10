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
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(' ')                
                x, y = data[1][1:-1].split(',')
                x, y = float(x), float(y)
                vertices = data[3:]
                vertices = list(map(int, vertices))
                graph.append(vertices)                                
    except Exception as e:
        print(e)        
    return graph

def construct_graph_nx(graph):
    G = nx.Graph()    
    for i in range(len(graph)):                        
        for v in graph[i]:
            G.add_edge(i+1,v)        
    return G

def plot_graph(graph, partitioned = False):
    """_summary_: visualize a graph

    Args:
        graph (_type_): _description_
    """
    G = construct_graph_nx(graph)
    nx.draw(G, with_labels = True)        
    plt.show()
    

def plot_partitioned_graph(graph, partition):
    color_map = list(map(lambda x: 'red' if x==0 else 'blue', partition))    
    G = construct_graph_nx(graph)    
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.show()
