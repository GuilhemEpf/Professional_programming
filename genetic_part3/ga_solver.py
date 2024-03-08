# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(generic genetic algorithm module)
"""
import random

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome (list[]): a list representing the individual's
            chromosome
            fitness (float): the individual's fitness (the higher the value,
            the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GAProblem:
    #in this class we call all function that needed to be change from the mastermind problem to the tsp problem. this is because we isolated these parts of the function
    # that the algorithm can be use for multiple problem. 

    """Defines a Genetic algorithm problem to be solved by ga_solver"""  
    def chromosome_fonction(self):
        pass
    def fitness_fonction(self, chromosome): 
        self.chromosome_fonction=chromosome
        pass
    def evolve_generation(self, population, parent1, parent2):
        pass
    def chromosome_mutation(self, indexind):
        pass


class GASolver:
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            problem (GAProblem): GAProblem to be solved by this ga_solver
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._problem = problem
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

#in this function we create a new chromosome and calculate its fitness, the list and the variable then constitue what we call an individual that we can add to a population. 
    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """
        for _ in range(pop_size): 
            chromosome=self._problem.chromosome_fonction()
            fitness =self._problem.fitness_fonction(chromosome)
            new_individual = Individual(chromosome, fitness)
            self._population.append(new_individual)
#this function serves to refresh the population with new individual which has chromosome with a better fitness score, in order to maximize our chance to get the right combinaison in the end.
#
    def evolve_for_one_generation(self):
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """
        self._population.sort(reverse=True) #we sort the population in descending order

        poptodelete = len(self._population) * 0.5  # Proportion of population kept
        self._population = self._population[:int(-poptodelete)]

        new_added_indiv=[]
        for i in range(len(self._population)): # here we take two random parent from the survivor and calculate the new
            # chromosome by taking a part of the first parent and a part of the second parent. 
            # The crossoverpoint is here to decide what part we take from each parent. le 1er parent prend la partie avant le crossover point et le deuxième sa partie après le crossoverpoint
            parent1, parent2 = random.sample(self._population, 2)
            while parent2 == parent1:
                parent2 = random.choice(self._population)

            new_chromosome = self._problem.evolve_generation(parent1,parent2)
            new_fitness=self._problem.fitness_fonction(new_chromosome)
            new_individual = Individual(new_chromosome, new_fitness) 
            new_added_indiv.append(new_individual)
        self._population = self._population + new_added_indiv

        #the mutation is a phenomen that happen randomly and that change one of the chromosome. the population scooted through and once the mutation happen the corresponding chromosome see its value xhanged
        for indexind in self._population:
            if len(self._population) != 50:
                if random.random() < self._mutation_rate:
                    new_chromosome=self._problem.chromosome_mutation(indexind)
                    new_fitness =self._problem.fitness_fonction(new_chromosome)
                    self._population.append(Individual(new_chromosome, new_fitness))

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        for individual in self._population:
            print(individual)

    def get_best_individual(self):
        """ Return the best Individual of the population """
        self._population.sort(reverse=True)
        best_individual = self._population[0]
        return best_individual

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        max_nb_of_generations=max_nb_of_generations
        for i in range (0,max_nb_of_generations):
            self.evolve_for_one_generation()
