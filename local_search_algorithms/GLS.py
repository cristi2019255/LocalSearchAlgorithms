from local_search_algorithms.FM import FM
from local_search_algorithms.utils import generate_random_solution
import numpy as np

def GLS(nr_of_runs = 25, graph = []):
    # hardcoded for testing only        
    ga = GA(graph)    
    return ga.resolve(population_size=10, nr_of_runs = nr_of_runs)

class GA:
    def __init__(self, graph):
        self.graph = graph
        self.population = []
        self.fitnesses = []
        self.solution_size = len(graph)    

    def resolve(self, population_size, nr_of_runs):
        self.initialise_population(population_size)
        
        for generation in range(nr_of_runs):
            #### crossover UX 1 child
            p1, p2 = np.random.choice(population_size, 2, replace= False)            
            offspring = self.uniform_crossover(self.population[p1], self.population[p2])
            
            ## mutation with FM
            offspring_genome, offspring_fitness = FM(offspring, self.graph)
            
            if offspring_fitness < max(self.fitnesses):
                self.population[np.argmax(self.fitnesses)] = offspring_genome
                self.fitnesses[np.argmax(self.fitnesses)] = offspring_fitness
        
                        
        return self.population[np.argmin(self.fitnesses)], min(self.fitnesses)

    def initialise_population(self,population_size = 10):        
        for _ in range(population_size):
            solution = generate_random_solution(self.solution_size)
            genome, fitness = FM(solution, self.graph)
            self.population.append(genome)
            self.fitnesses.append(fitness)
            
    def uniform_crossover(self, parent1, parent2):
        ### check hamming distance of a parent if bigger than N/2 flip all bits and then do the crossover
        
        probabilities = np.random.rand(self.solution_size) < 0.5
        offspring = np.copy(parent1)           
        offspring[probabilities] = parent2[probabilities]        
        ### to check if consistent solution
        return offspring