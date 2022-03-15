import re
def read_graph_from_file(filename = ''):
    """ Reading a graph from file

    Args:
        filename (string, optional): The filename in which the graph is stored. Defaults to ''.

    Returns:
        list of lists, list: The graph & vertices positions in plane
    """
    try:
        graph = []
        positions = []
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                data = re.split(r"\s+", line.strip())                           
                x, y = data[1][1:-1].split(',')
                x, y = float(x), float(y)
                positions.append((x,y))
                vertices = data[3:]
                vertices = list(map(lambda x: x-1,list(map(int, vertices))))                
                graph.append(vertices)                                
            file.close()
    except Exception as e:
        print(e)       
    return graph, positions
