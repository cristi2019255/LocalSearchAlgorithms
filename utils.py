from datetime import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm

NR_OF_RUNS = 25   
    
def compute_statistics():    
    plt.title('Comparison of local search algorithms')
    experiments = ['MLS','ILS_01', 'ILS_05', 'ILS_10', 'GLS_5', 'GLS_10','GLS_20']
    file_names = list(map(lambda x: './Results/' + x + '.txt', experiments))
    experimental_data = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            line = file.readline()            
            optimums = list(map(int,line.strip().split(' ')))
            file.close()    
        experimental_data.append(optimums)
    
    plt.boxplot(experimental_data, labels=experiments)    
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