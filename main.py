from datetime import datetime
from graph_tools.generator import generate_graph
from graph_tools.ploter import plot_graph, plot_partitioned_graph
from graph_tools.reader import read_graph_from_file
from local_search_algorithms.GLS import GLS
from local_search_algorithms.ILS import ILS
from local_search_algorithms.MLS import MLS
from utils import compute_statistics, experiment


FILE_NAME = './G500.txt'
NR_OF_FM_CALLS = 10000

def test_FM(graph, positions):        
    start = datetime.now()
    solution, cuts = MLS(graph = graph, nr_of_calls=1000) #GLS(graph = graph, nr_of_calls=1000, population_size=20)
    end = datetime.now()
    print('Min cuts: ' + str(cuts))
    print('Run time: ' + str(end-start))    
    plot_partitioned_graph(graph = graph, partition= solution, positions=positions)    

def main():
    graph, positions = read_graph_from_file(filename=FILE_NAME)                    
    #graph, positions = generate_graph(500,random=True)                       
    #plot_graph(graph, positions)       
    #test_FM(graph, positions)
    #experiment('./Results/MLS.txt', MLS)(graph = graph)
    #experiment('./Results/ILS_01.txt', ILS)(graph = graph, probability = 0.01 , nr_of_calls = NR_OF_FM_CALLS)
    #experiment('./Results/ILS_05.txt', ILS)(graph = graph, probability = 0.05 , nr_of_calls = NR_OF_FM_CALLS)
    #experiment('./Results/ILS_10.txt', ILS)(graph = graph, probability = 0.1 , nr_of_calls = NR_OF_FM_CALLS)
    experiment('./Results/ILS_20.txt', ILS)(graph = graph, probability = 0.2 , nr_of_calls = NR_OF_FM_CALLS)
    #experiment('./Results/GLS_20.txt', GLS)(graph = graph, population_size = 5 , nr_of_calls = NR_OF_FM_CALLS)   
    #experiment('./Results/GLS_20.txt', GLS)(graph = graph, population_size = 10, nr_of_calls = NR_OF_FM_CALLS)
    #experiment('./Results/GLS_20.txt', GLS)(graph = graph, population_size = 20, nr_of_calls = NR_OF_FM_CALLS)
    compute_statistics()
    
if __name__ == '__main__':
    main()