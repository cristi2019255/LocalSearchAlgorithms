import matplotlib.pyplot as plt
import networkx as nx

def construct_graph_nx(graph):
    G = nx.Graph()    
    for i in range(len(graph)):                     
        for v in graph[i]:
            G.add_edge(i, v)        
    return G

def plot_graph(graph, positions):
    """ Visualize a graph

    Args:
        graph (list of lists): The graph to be visualized
        positions (list of (float,float)): Vertices positions in plane 
    """
    G = construct_graph_nx(graph)
    nx.draw(G, with_labels = True, pos = positions)        
    plt.show()
    

def plot_partitioned_graph(graph, partition, positions):    
    """ Visualize the partitioned graph

    Args:
        graph (list of lists): The graph to be visualized
        positions (list of (float,float)): Vertices positions in plane 
        partition (list): The partition
    """
    color_map = []
    G = construct_graph_nx(graph)    
    for node in G:
        if partition[node] == 0:
            color_map.append('red')
        else:
            color_map.append('blue')
                    
    nx.draw(G, node_color=color_map, with_labels=True, pos=positions)
    plt.show()            
