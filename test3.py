# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""
import random
import mastermind as mm 


class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm 

        Args:
            chromosome (list[]): a list representing the individual's chromosome
            fitness (float): the individual's fitness (the higher, the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GASolver:
    def __init__(self, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals 
        
        Args:
            pop_size (integer): number of individuals in the population. 
        """
        for i in range (pop_size):
            chromosome = MATCH.generate_random_guess()  # We create a random chromosome
            fitness = MATCH.rate_guess(chromosome)  # We evaluate the chromosome
            new_individual = Individual(chromosome, fitness)   # New random individual
            self._population.append(new_individual)


    def evolve_for_one_generation(self):
        self._population.sort(key=lambda x: x.fitness, reverse=True)
        #-	Selection: Remove x% of population (less adapted)
        x = 50 
        x_purcent_index = len(self._population) * x / 100  #proportion of population kept
        self._population = self._population[:int(-x_purcent_index)] 

        #-   Reproduction: Recreate the same quantity by crossing the surviving ones 
        new_chromosomes=[]
        
        for i in range(len(self._population)):
        # each time we have a chriomosome in our population (here 25 times):
            parent1, parent2 = random.sample(self._population, 2) 
            crossing_point = random.randrange(0, len(parent1.chromosome))   # we take a random crossing point to break parent's chromosome
            new_chrom = parent1.chromosome[0:crossing_point] + parent2.chromosome[crossing_point:]
            new_individual = Individual(new_chrom, MATCH.rate_guess(new_chrom)) 
            new_chromosomes.append(new_individual)
            
            number = random.random() #proba uniformly distributed. 
            valid_colors = mm.get_possible_colors()
            p = self._mutation_rate  #we chose 0.1 as a probability default value
        self._population=self._population + new_chromosomes  #we match 50% of best former population and new population

        #-	Mutation: For each new Individual, mutate with probability mutation_rate i.e., mutate it if a random value is below mutation_rate
        for individual in self._population:
            while len(self._population)!=50:  
                if number < p:  #if the random number is under the probability, then we take the action, if not, nothing happens
                    pos = random.randint(0,len(individual.chromosome)-1)  
                    new_gene = random.choice(valid_colors)
                    new_chrom = individual.chromosome[0:pos] + [new_gene] + individual.chromosome[pos+1:]  
                    self._population.append(Individual(new_chrom, MATCH.rate_guess(new_chrom))) #new fitness calculation


    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self):
        """ Return the best Individual of the population """
        results=[]
        results = self._population
        results.sort(key=lambda x: x.fitness, reverse=True) #Decreasing Order compared to the fitness values. 
        return results[0]  

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=12.0):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        for i in range (0,max_nb_of_generations): 
            score=self.evolve_for_one_generation()  #we take the score for this population
            if score==threshold_fitness:
                break   #break when we have the best score

    

MATCH = mm.MastermindMatch(secret_size=4) 
solver=GASolver()
solver.reset_population()
solver.evolve_until(threshold_fitness=MATCH.max_score())
best = solver.get_best_individual()
print(f"Best Guess {best.chromosome}")
print(f"Problem solved ? {MATCH.is_correct(best.chromosome)}")   #if we get true it is a success