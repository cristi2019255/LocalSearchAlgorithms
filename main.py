from datetime import datetime
from turtle import pos, position
from local_search_algorithms.GLS import GLS
from local_search_algorithms.ILS import ILS
from local_search_algorithms.MLS import MLS
from utils import generate_graph, plot_graph, plot_partitioned_graph, read_graph_from_file

FILE_NAME = './G503.txt'
LOCAL_SEARCHERS = [MLS, ILS, GLS]

def experiments():
    graph, positions = read_graph_from_file(filename=FILE_NAME)
    #plot_graph(graph, positions)
    for ls in LOCAL_SEARCHERS:
        solution, cuts = ls(graph = graph)
        print(f'Minimum nr of cuts is: {cuts}')
        print(f'Solution is: {solution}')
        #plot_partitioned_graph(graph = graph, partition= solution)    


def test_FM():
    #graph,  positions = read_graph_from_file(filename=FILE_NAME)            
    graph, positions = generate_graph(500,fully_connected=True)        
    #plot_graph(graph, positions)    
    start = datetime.now()
    solution, cuts = GLS(graph = graph)
    end = datetime.now()
    print('Min cuts: ' + str(cuts))
    print('Run time: ' + str(end-start))    
    plot_partitioned_graph(graph = graph, partition= solution, positions=positions)    

def main():
    experiments()
    #test_FM()

if __name__ == '__main__':
    main()