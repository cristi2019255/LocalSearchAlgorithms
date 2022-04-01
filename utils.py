from datetime import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import time
import numpy as np

from local_search_algorithms.FM import FM_pass
from local_search_algorithms.GLS import GLS
from local_search_algorithms.ILS import ILS, adaptive_ILS
from local_search_algorithms.MLS import MLS

NR_OF_RUNS = 25  
NR_OF_FM_CALLS = 10000
RESULTS_DIRECTORY = './Results/' 
EXPERIMENTS = ['MLS', 'ILS_15', 'adaptive_ILS','GLS_50']
    
def compute_statistics(title = 'comparison of local search algorithms', x_label = 'local searcher', y_label = 'optimum cut', experiments = EXPERIMENTS):
    file_names = list(map(lambda x: RESULTS_DIRECTORY + x + '.txt', experiments))
    experimental_data = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            line = file.readline()            
            optimums = list(map(int,line.strip().split(' ')))
            file.close()    
        experimental_data.append(optimums)
    
    
    fig = plt.figure()
    plt.title('Comparison of local search algorithms')
    plt.boxplot(experimental_data, labels=experiments)
    plt.xlabel(x_label)
    plt.ylabel(y_label)    
    fig_name = './Results/' + title + '.png'
    fig.savefig(fig_name, dpi=fig.dpi)
    #plt.show()

def experiment(results_file_name, func):
    def experiment_wrapper(*args, **kwargs):                
        same_region_proportions = []
        optimum_cuts = []
        with open(results_file_name, 'w') as file:
            start = datetime.now()
            for _ in tqdm(range(NR_OF_RUNS)): 
                if func.__name__ == 'ILS':
                    _ , optimum_cut, same_region_proportion = func(*args, **kwargs)
                    same_region_proportions.append(same_region_proportion)
                else:               
                    _, optimum_cut = func(*args, **kwargs)            

                file.write(str(optimum_cut) + ' ')
                optimum_cuts.append(optimum_cut)                                                                          
            end = datetime.now()
            
            print('Run time: ' + str(end-start))                                 
            file.write('\nAverage optimum cut: ' + str(round(np.mean(optimum_cuts),4)) + ' (' + str(round(np.std(optimum_cuts),4)) + ') ')
            file.write('\nMedian optimum cut: ' + str(round(np.median(optimum_cuts),4)))
            file.write('\nRun time:' + str(end-start))
            if func.__name__ == 'ILS':
                file.write('\nSame region proportion: ' + str(same_region_proportions))
                file.write('\nAverage same region proportion: ' + str(round(np.mean(same_region_proportions),4)) + ' (' + str(round(np.std(same_region_proportions),4)) + ') ')
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
        _, optimum_ils, _ = ILS(graph=graph, probability=ils_probability, stopping_criterion=create_stop_after_delta_time(end_time))
        
        print('GLS ...')
        end_time = time() + delta_time
        _, optimum_gls = GLS(graph=graph, population_size= gls_population_size, stopping_criterion=create_stop_after_delta_time(end_time))
        
        mls_optimums.append(optimum_mls)
        ils_optimums.append(optimum_ils)
        gls_optimums.append(optimum_gls)
        delta_times.append(delta_time)
        
    ### saving the results
    with open( (RESULTS_DIRECTORY + 'delta_time.txt'), 'w') as file:
        file.write('ILS probability: ' + str(ils_probability) + ', GLS population size: ' + str(gls_population_size) + '\n')
        file.write('Delta time: ' + str(delta_times) + '\n')
        file.write(str(mls_optimums) + '\n')
        file.write(str(ils_optimums) + '\n')
        file.write(str(gls_optimums) + '\n\n')        
        file.write('\nAverage delta time: ' + str(round(np.mean(delta_times),4)) + ' (' + str(round(np.std(delta_times),4)) + ') ')
        file.write('\nAverage mls optimum: ' + str(round(np.mean(mls_optimums),4)) + ' (' + str(round(np.std(mls_optimums),4)) + ') ')
        file.write('\nAverage ils optimum: ' + str(round(np.mean(ils_optimums),4)) + ' (' + str(round(np.std(ils_optimums),4)) + ') ')
        file.write('\nAverage gls optimum: ' + str(round(np.mean(gls_optimums),4)) + ' (' + str(round(np.std(gls_optimums),4)) + ') ')
        file.write('\nMedian mls optimum: ' + str(round(np.median(mls_optimums),4)))
        file.write('\nMedian ils optimum: ' + str(round(np.median(ils_optimums),4)))
        file.write('\nMedian gls optimum: ' + str(round(np.median(gls_optimums),4)))
        file.close()
    
    compute_statistics(title = 'Comparison of local searchers with fixed delta_time', x_label = 'local searcher', y_label = 'Optimum cuts', experiments = ['MLS', 'ILS_' + str(ils_probability), 'GLS'])
    fig = plt.figure()
    plt.title('Delta time')
    plt.plot(delta_times)
    plt.xlabel('Run')
    plt.ylabel('Delta time')    
    fig_name = RESULTS_DIRECTORY + 'Delta_times' + '.png'
    fig.savefig(fig_name, dpi=fig.dpi)
    #plt.show()

def experiments_stop_after_calls(graph):
    #experiment(RESULTS_DIRECTORY + 'MLS.txt', MLS)(graph = graph, stopping_criterion = stop_after_calls)
    
    # experiments ILS
    experiment(RESULTS_DIRECTORY + 'ILS_004.txt', ILS)(graph = graph, probability = 0.004 , stopping_criterion = stop_after_calls)
    experiment(RESULTS_DIRECTORY + 'ILS_05.txt', ILS)(graph = graph, probability = 0.05 , stopping_criterion = stop_after_calls)
    experiment(RESULTS_DIRECTORY + 'ILS_10.txt', ILS)(graph = graph, probability = 0.1 , stopping_criterion = stop_after_calls)
    experiment(RESULTS_DIRECTORY + 'ILS_15.txt', ILS)(graph = graph, probability = 0.15 , stopping_criterion = stop_after_calls)
    experiment(RESULTS_DIRECTORY + 'ILS_20.txt', ILS)(graph = graph, probability = 0.2 , stopping_criterion = stop_after_calls)
    experiment(RESULTS_DIRECTORY + 'ILS_50.txt', ILS)(graph = graph, probability = 0.5 , stopping_criterion = stop_after_calls)
    
    #experiment(RESULTS_DIRECTORY + 'adaptive_ILS_pmin_01_alpha_05_beta_05_reward_binary.txt', adaptive_ILS)(graph = graph, stopping_criterion = stop_after_calls, P_min = 0.1, alpha = 0.5, beta = 0.5, operators = [0.004, 0.05, 0.1, 0.15, 0.2, 0.5], reward_binary = True)
    #experiment(RESULTS_DIRECTORY + 'adaptive_ILS_pmin_01_alpha_05_beta_05_reward_non_binary.txt', adaptive_ILS)(graph = graph, stopping_criterion = stop_after_calls, P_min = 0.1, alpha = 0.5, beta = 0.5, operators = [0.004, 0.05, 0.1, 0.15, 0.2, 0.5], reward_binary = False)
    
    #experiment(RESULTS_DIRECTORY + 'adaptive_ILS_pmin_01_alpha_08_beta_05_reward_binary.txt', adaptive_ILS)(graph = graph, stopping_criterion = stop_after_calls, P_min = 0.1, alpha = 0.8, beta = 0.5, operators = [0.004, 0.05, 0.1, 0.15, 0.2, 0.5], reward_binary = True)
    #experiment(RESULTS_DIRECTORY + 'adaptive_ILS_pmin_01_alpha_05_beta_08_reward_binary.txt', adaptive_ILS)(graph = graph, stopping_criterion = stop_after_calls, P_min = 0.1, alpha = 0.5, beta = 0.8, operators = [0.004, 0.05, 0.1, 0.15, 0.2, 0.5], reward_binary = True)
        
    #experiment(RESULTS_DIRECTORY + 'GLS_50.txt', GLS)(graph = graph, population_size = 50, stopping_criterion = stop_after_calls)
    
    #compute_statistics(title = 'Comparison of iterative local searchers with fixed number of FM_pass calls', x_label = 'local searcher', y_label = 'Optimum cuts', experiments = ['MLS', 'ILS_004', 'ILS_05', 'ILS_10', 'ILS_15', 'ILS_20', 'ILS_50'])
    #compute_statistics(title = 'Comparison of local searchers with fixed number of FM_pass calls', x_label = 'local searcher', y_label = 'Optimum cuts', experiments = ['MLS', 'ILS_15', 'GLS_50'])
    #compute_statistics(title = 'Comparison of adaptive ILS with fixed number of FM_pass calls', x_label = 'local searcher', y_label = 'Optimum cuts', experiments = ['ILS_15','ILS_pmin_01_alpha_05_beta_05_reward_binary', 'ILS_pmin_01_alpha_05_beta_05_reward_non_binary', 'ILS_pmin_01_alpha_08_beta_05_reward_binary', 'ILS_pmin_01_alpha_05_beta_08_reward_binary'])