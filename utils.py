from datetime import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import time

from local_search_algorithms.FM import FM_pass
from local_search_algorithms.GLS import GLS
from local_search_algorithms.ILS import ILS
from local_search_algorithms.MLS import MLS

NR_OF_RUNS = 25  
NR_OF_FM_CALLS = 10000
RESULTS_DIRECTORY = './Results' 
#EXPERIMENTS = ['MLS','ILS_01', 'ILS_05', 'ILS_10', 'ILS_15', 'ILS_20', 'ILS_50','adaptive_ILS', 'GLS_5', 'GLS_10','GLS_20', 'GLS_50', 'GLS_100', 'GLS_300', 'GLS_500']
EXPERIMENTS = ['MLS', 'ILS_15', 'adaptive_ILS','GLS_50']
    
def compute_statistics():            
    file_names = list(map(lambda x: './Results/' + x + '.txt', EXPERIMENTS))
    experimental_data = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            line = file.readline()            
            optimums = list(map(int,line.strip().split(' ')))
            file.close()    
        experimental_data.append(optimums)
    
    plt.title('Comparison of local search algorithms')
    plt.boxplot(experimental_data, labels=EXPERIMENTS)    
    plt.show()

def experiment(results_file_name, func):
    def experiment_wrapper(*args, **kwargs):                
        with open(results_file_name, 'w') as file:
            start = datetime.now()
            for _ in tqdm(range(NR_OF_RUNS)):                
                solution, optimum_cuts = func(*args, **kwargs)            
                file.write(str(optimum_cuts) + ' ')
                                      
            end = datetime.now()
            print('Run time: ' + str(end-start))                     
            file.write('\nRun time:' + str(end-start))
            file.close()
        print(f'Done, take a look in {results_file_name} ...')
    
    return experiment_wrapper

def stop_after_calls():
    """
    Stopping after a number of FM_pass calls criterion
    Returns:
        bool
    """
    return FM_pass.call_count >= NR_OF_FM_CALLS 


def create_stop_after_delta_time(end_time):
    def stop_after_delta_time():
        return time() >= end_time
    
    return stop_after_delta_time    

def experiments_delta_time(graph, ils_probability = 0.15, gls_population_size = 50):
    ### experiments with stopping criterion delta_time     
    mls_optimums, ils_optimums, gls_optimums = [], [], []
    delta_times = []
    for _ in tqdm(range(25)):
        print('MLS ...')
        start = time()
        _, optimum_mls = MLS(graph = graph, stopping_criterion=stop_after_calls)        
        delta_time = time() - start

        print('ILS ...')        
        end_time = time() + delta_time
        _, optimum_ils = ILS(graph=graph, probability=ils_probability, stopping_criterion=create_stop_after_delta_time(end_time))
        
        print('GLS ...')
        end_time = time() + delta_time
        _, optimum_gls = GLS(graph=graph, population_size= gls_population_size, stopping_criterion=create_stop_after_delta_time(end_time))
        
        mls_optimums.append(optimum_mls)
        ils_optimums.append(optimum_ils)
        gls_optimums.append(optimum_gls)
        delta_times.append(delta_time)
        
    ### saving the results
    with open('./Results/delta_time.txt', 'w') as file:
        file.write('ILS probability: ' + str(ils_probability) + ', GLS population size: ' + str(gls_population_size) + '\n')
        file.write('Delta time: ' + str(delta_times) + '\n')
        file.write(str(mls_optimums) + '\n')
        file.write(str(ils_optimums) + '\n')
        file.write(str(gls_optimums) + '\n\n')
        file.close()