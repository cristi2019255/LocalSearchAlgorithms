from math import ceil, floor
from random import sample
from local_search_algorithms.FM import FM, FM_pass
from local_search_algorithms.utils import generate_random_solution
import numpy as np

def GLS(stopping_criterion, population_size = 5, graph = []):    
    """Genetic local search for graph bipartitioning problem

    Args:
        stopping_criterion (()-> bool)
        population_size (int, optional): The population size of the genetic algorithm. Defaults to 5.
        graph (list, optional): Defaults to [].

    Returns:
        (list, int): best found partition & min number of cuts
    """
    FM_pass.set_count_calls(0)
    ga = GA(graph, stopping_criterion)    
    solution, optimum = ga.resolve(population_size=population_size)
    print(FM_pass.call_count)
    FM_pass.set_count_calls(0)
    return solution, optimum

class GA:
    def __init__(self, graph, stopping_criterion):
        self.graph = graph
        self.N = len(graph)
        self.population = []
        self.fitnesses = []
        self.solution_size = len(graph)    
        self.stopping_criterion = stopping_criterion

    def resolve(self, population_size):         
        self.initialise_population(population_size)
        
        best_cut = min(self.fitnesses)            
                
        while not self.stopping_criterion():
            #### crossover UX 1 child
            p1, p2 = np.random.choice(population_size, 2, replace= False)            
            offspring = self.uniform_crossover(self.population[p1], self.population[p2])
            
            ## mutation with FM local search
            offspring_genome, offspring_fitness = FM(self.stopping_criterion, offspring, self.graph)            
            
            if offspring_fitness < max(self.fitnesses):
                self.population[np.argmax(self.fitnesses)] = offspring_genome
                self.fitnesses[np.argmax(self.fitnesses)] = offspring_fitness
                        
            if best_cut > offspring_fitness:
                best_cut = offspring_fitness
                print(f'New best optimum: {best_cut}')                            
                   
        return self.population[np.argmin(self.fitnesses)], best_cut

    def initialise_population(self,population_size = 10):        
        print('Initializing population ...')
        for _ in range(population_size):
            solution = generate_random_solution(self.solution_size)
            genome, fitness = FM(self.stopping_criterion, solution, self.graph)
            self.population.append(genome)
            self.fitnesses.append(fitness)
                
    def uniform_crossover(self, parent1, parent2):
        """Uniform crossover for graph bipartitioning solutions
           Copy to the offspring the genes of the parents where they are the same
           Where parents are different with probability 0.5, flip the markers
           If parents differ in hamming distance by more than vertices/2, flip the representation for a parent
           
        Args:
            parent1 (list)
            parent2 (list) 

        Returns:
            list: The generated offspring
        """                
        assert(len(parent1) == len(parent2))
        assert(len(parent1) == self.N)        
        
        ### Checking hamming distance of a parent if bigger than N/2 flip all bits and then do the crossover
        if (self.hamming_distance(parent1, parent2) > int(self.N/2)):
            parent2 = self.flip(parent2)            
        
        
        offspring = np.copy(parent1)
        
        # getting the set of indexes where parents disagree
        disagreement_zeros, disagreement_ones = [], []        
        for i in range(self.N):
            if not parent1[i] == parent2[i]:                
                if parent1[i] == 0:
                    disagreement_zeros.append(i)
                else:  
                    disagreement_ones.append(i)
        
        assert(len(disagreement_zeros) == len(disagreement_ones))
        
        p = np.random.randint(0,1)
        k = int(0.5 * len(disagreement_ones)) if len(disagreement_ones) % 2 == 0 else int(ceil(0.5 * len(disagreement_ones)))  if p == 0 else int(floor(0.5 * len(disagreement_ones)))                                                   
        ones_indexes_sample = sample(disagreement_ones, k=k) 
        zeros_indexes_sample = sample(disagreement_zeros, k=k) 
        
        for i in range(k):
            offspring[ones_indexes_sample[i]] = 0
            offspring[zeros_indexes_sample[i]] = 1
        
        assert(np.sum(offspring) == int(self.N/2))
        
        return offspring
        
    def hamming_distance(self, x, y):
        """ 
            Calculating the Hamming distance between to bit lists
        """
        assert(len(x) == len(y))    
        distance = 0
        for i in range(len(x)):
            distance += not (x[i] == y[i])
        return distance
    
    def flip(self, sol):
        """ 
            Fliping the markers for the solution 1 -> 0 & 0 -> 1
        """
        for i in range(len(sol)):
            sol[i] = 1 - sol[i]
        return sol