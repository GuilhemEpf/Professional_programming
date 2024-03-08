# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem
import cities
import random

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""
    def __init__(self):
        self.city_dict = cities.load_cities("C:/Users/guilh/OneDrive/Bureau/A4/Professional Programming/TP3/Professional_programming/genetic_part3/cities.txt") #using cities.load_cities, we are able to read the text file summarizing the locations of the cities
        self.chromosome = cities.default_road(self.city_dict)
        self.fitness = - cities.road_length(self.city_dict, self.chromosome)
        self.possibilities = cities.default_road(self.city_dict)
#in the two following function we calculate the chromosome and fitness in the way that is unique to this problem
    def chromosome_fonction(self):
        chromosome= cities.default_road(self.city_dict)
        random.shuffle(chromosome)
        return chromosome
    
    def fitness_fonction(self, chromosome): 
        fitness = -cities.road_length(self.city_dict, chromosome)
        return fitness
        
    def evolve_generation(self, parent1, parent2):
        #in the case of  this probleme the crossover point is specifically half  the size of the chromosome to simplify.  
        crossover_point = int((len(parent1.chromosome))/2)
        new_chromosome = parent1.chromosome[0:crossover_point] + parent2.chromosome[crossover_point:]
        #here we check that all cities have been included in the process, and none left out
        cities_left = [city for city in parent2.chromosome if city not in new_chromosome]
        new_chromosome.extend(cities_left)




        return new_chromosome 


#in this problem in case the mutation happen, we exchange the position of two random value of the mutated chromosome
    def chromosome_mutation(self, indexind):
        index1, index2 = random.sample(range(len(indexind.chromosome)), 2)  
        while index1==index2: # we need to make sure that the two index are different,else it would be no different than no mutation 
            index2=random.randint(0,len(new_chromosome)-1)
            new_chromosome[index1],new_chromosome[index2] = new_chromosome[index2],new_chromosome[index1]
        new_chromosome = indexind.chromosome.copy()
        new_chromosome[index1], new_chromosome[index2] = new_chromosome[index2], new_chromosome[index1]
        return new_chromosome



if __name__ == '__main__':

    from ga_solver import GASolver

    city_dict = cities.load_cities("C:/Users/guilh/OneDrive/Bureau/A4/Professional Programming/TP3/Professional_programming/genetic_part3/cities.txt")
    problem = TSProblem()
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until()
    cities.draw_cities(city_dict, solver.get_best_individual().chromosome)
