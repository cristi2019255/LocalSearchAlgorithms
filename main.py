from datetime import datetime
from graph_tools.generator import generate_graph
from graph_tools.ploter import plot_graph, plot_partitioned_graph
from graph_tools.reader import read_graph_from_file
from local_search_algorithms.GLS import GLS
from utils import experiments_delta_time, experiments_stop_after_calls, stop_after_calls


FILE_NAME = './G500.txt'

def test_FM(graph, positions):        
    start = datetime.now()
    solution, cuts = GLS(graph = graph, stopping_criterion=stop_after_calls, population_size=100)
    end = datetime.now()
    print('Min cuts: ' + str(cuts))
    print('Run time: ' + str(end-start))    
    plot_partitioned_graph(graph = graph, partition= solution, positions=positions)    


def main():
    graph, positions = read_graph_from_file(filename=FILE_NAME)  
                      
    #graph, positions = generate_graph(500,random=True)                       
    #plot_graph(graph, positions)       
    #test_FM(graph, positions)
    
    experiments_stop_after_calls(graph)    
    
    #experiments_delta_time(graph)         
    
if __name__ == '__main__':
    main()