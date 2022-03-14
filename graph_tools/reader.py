import re
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
