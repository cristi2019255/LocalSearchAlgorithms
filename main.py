from datetime import datetime
from graph_tools.generator import generate_graph
from graph_tools.ploter import plot_graph, plot_partitioned_graph
from graph_tools.reader import read_graph_from_file
from local_search_algorithms.FM import FM_pass
from local_search_algorithms.GLS import GLS
from local_search_algorithms.ILS import ILS, adaptive_ILS
from local_search_algorithms.MLS import MLS
from utils import compute_statistics, experiment, experiments_delta_time, stop_after_calls


FILE_NAME = './G500.txt'

def test_FM(graph, positions):        
    start = datetime.now()
    solution, cuts = GLS(graph = graph, nr_of_calls=10000, population_size=100)
    end = datetime.now()
    print('Min cuts: ' + str(cuts))
    print('Run time: ' + str(end-start))    
    plot_partitioned_graph(graph = graph, partition= solution, positions=positions)    

def main():
    graph, positions = read_graph_from_file(filename=FILE_NAME)                    
    #graph, positions = generate_graph(500,random=True)                       
    #plot_graph(graph, positions)       
    #test_FM(graph, positions)
    #experiment('./Results/MLS.txt', MLS)(graph = graph, stopping_criterion = stop_after_calls)
    
    #experiment('./Results/ILS_01.txt', ILS)(graph = graph, probability = 0.01 , stopping_criterion = stop_after_calls)
    #experiment('./Results/ILS_05.txt', ILS)(graph = graph, probability = 0.05 , stopping_criterion = stop_after_calls)
    #experiment('./Results/ILS_10.txt', ILS)(graph = graph, probability = 0.1 , stopping_criterion = stop_after_calls)
    experiment('./Results/ILS_15.txt', ILS)(graph = graph, probability = 0.15 , stopping_criterion = stop_after_calls)
    #experiment('./Results/ILS_20.txt', ILS)(graph = graph, probability = 0.2 , stopping_criterion = stop_after_calls)
    #experiment('./Results/ILS_50.txt', ILS)(graph = graph, probability = 0.5 , stopping_criterion = stop_after_calls)
    #experiment('./Results/adaptive_ILS.txt', adaptive_ILS)(graph = graph, stopping_criterion = stop_after_calls, P_min = 0.1, alpha = 0.5, beta = 0.5, operators = [0.01, 0.05, 0.1, 0.2])
    
    #experiment('./Results/GLS_5.txt', GLS)(graph = graph, population_size = 5 , stopping_criterion = stop_after_calls)   
    #experiment('./Results/GLS_10.txt', GLS)(graph = graph, population_size = 10, stopping_criterion = stop_after_calls)
    #experiment('./Results/GLS_20.txt', GLS)(graph = graph, population_size = 20, stopping_criterion = stop_after_calls)
    #experiment('./Results/GLS_50.txt', GLS)(graph = graph, population_size = 50, stopping_criterion = stop_after_calls)
    #experiment('./Results/GLS_100.txt', GLS)(graph = graph, population_size = 100, stopping_criterion = stop_after_calls)
    #experiment('./Results/GLS_300.txt', GLS)(graph = graph, population_size = 300, stopping_criterion = stop_after_calls)
    #experiment('./Results/GLS_500.txt', GLS)(graph = graph, population_size = 500, stopping_criterion = stop_after_calls)
    
    
    #experiments_delta_time(graph) 
    
    #compute_statistics()
    
if __name__ == '__main__':
    main()