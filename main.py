from local_search_algorithms.GLS import GLS
from local_search_algorithms.ILS import ILS
from local_search_algorithms.MLS import MLS
from utils import plot_graph, plot_partitioned_graph, read_graph_from_file

FILE_NAME = './G500.txt'
LOCAL_SEARCHERS = [MLS, ILS, GLS]

def experiments():
    graph, _ = read_graph_from_file(filename=FILE_NAME)
    plot_graph(graph)
    for ls in LOCAL_SEARCHERS:
        solution, cuts = ls(graph = graph)
        print(f'Minimum nr of cuts is: {cuts}')
        plot_partitioned_graph(graph = graph, partition= solution)    


def test_FM():
    graph, max_degree = read_graph_from_file(filename=FILE_NAME)            
    solution, cuts = MLS(graph = graph, max_degree = max_degree)
    plot_partitioned_graph(graph = graph, partition= solution)    

def main():
    #experiments()
    test_FM()

if __name__ == '__main__':
    main()