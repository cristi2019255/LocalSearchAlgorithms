from random import sample
from local_search_algorithms.FM import FM, FM_pass
from local_search_algorithms.utils import generate_random_solution
import numpy as np

def GLS(nr_of_calls = 100, population_size = 5, graph = []):    
    FM_pass.set_count_calls(0)
    ga = GA(graph)    
    solution, optimum = ga.resolve(population_size=population_size, nr_of_calls = nr_of_calls)
    FM_pass.set_count_calls(0)
    return solution, optimum

class GA:
    def __init__(self, graph):
        self.graph = graph
        self.N = len(graph)
        self.population = []
        self.fitnesses = []
        self.solution_size = len(graph)    

    def resolve(self, population_size, nr_of_calls):         
        self.initialise_population(population_size)
        
        best_cut = min(self.fitnesses)            
                
        while FM_pass.call_count <= nr_of_calls: # making exactly nr_of_calls of FM_pass
            #### crossover UX 1 child
            p1, p2 = np.random.choice(population_size, 2, replace= False)            
            offspring = self.uniform_crossover(self.population[p1], self.population[p2])
            
            ## mutation with FM
            offspring_genome, offspring_fitness = FM(offspring, self.graph)            
            
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
            genome, fitness = FM(solution, self.graph)
            self.population.append(genome)
            self.fitnesses.append(fitness)
            
    def uniform_crossover(self, parent1, parent2):
        ### Checking hamming distance of a parent if bigger than N/2 flip all bits and then do the crossover
        assert(len(parent1) == len(parent2))
        assert(len(parent1) == self.N)        
        
        if (self.hamming_distance(parent1, parent2) > int(self.N/2)):
            parent2 = self.flip(parent2)            
        
        probabilities = np.random.rand(self.solution_size) < 0.5
        offspring = np.copy(parent1)           
        zeros_indxes, ones_indxes = [], []
        count_zeros = 0
        
        for i in range(self.N):            
            if probabilities[i] and not (parent1[i] == parent2[i]):
                offspring[i] = parent2[i]
                if offspring[i] == 0:
                    zeros_indxes.append(i)
                else:
                    ones_indxes.append(i)
            if offspring[i] == 0:
                count_zeros += 1            
        
        ### Checking if consistent solution
        if not (count_zeros == int(self.N/2)):            
            offspring = self.correct_solution(offspring, zeros_indxes, ones_indxes, count_zeros)                
        
        return offspring
    
    def correct_solution(self, solution, zeros, ones, count_zeros):        
        ### Ensuring that mutated solutions are still valid     
        diff = abs(count_zeros - int(self.N / 2))
        c = sample(ones, k=diff)  if (count_zeros < int(self.N/2)) else sample(zeros, k=diff)    
        for i in c:
            solution[i] = 1 - solution[i]     
            
        return solution
    
    def hamming_distance(self, x, y):
        assert(len(x) == len(y))    
        d = 0
        for i in range(len(x)):
            d += not (x[i] == y[i])
        return d
    
    def flip(self, sol):
        for i in range(len(sol)):
            sol[i] = 1 - sol[i]
        return sol