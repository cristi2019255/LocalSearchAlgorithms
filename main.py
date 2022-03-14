from datetime import datetime
from local_search_algorithms.MLS import MLS
from utils import compute_statistics, generate_graph, plot_graph, plot_partitioned_graph, read_graph_from_file, save_graph, test_GLS, test_ILS, test_MLS

FILE_NAME = './G500.txt'

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
    test_MLS(graph)
    #test_ILS(graph = graph, results_file_name= './Results/ILS_01.txt', probability = 0.01)
    #test_ILS(graph = graph, results_file_name= './Results/ILS_05.txt', probability = 0.05)
    #test_ILS(graph = graph, results_file_name= './Results/ILS_10.txt', probability = 0.1)
    #test_GLS(graph = graph, results_file_name= './Results/GLS_5.txt', population_size= 5)
    #test_GLS(graph = graph, results_file_name= './Results/GLS_10.txt', population_size= 10)
    #test_GLS(graph = graph, results_file_name= './Results/GLS_20.txt', population_size= 20)
    #compute_statistics()
    
if __name__ == '__main__':
    main()