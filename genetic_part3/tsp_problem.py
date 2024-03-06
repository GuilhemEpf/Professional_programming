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
    def chromosome(self):
        chromosome= cities.default_road(city_dict)
        random.shuffle(chromosome)

        return chromosome
    def fitness(self, chromosome): 
        fitness = -cities.road_length(city_dict, chromosome)
        return fitness
        
    def evolve_generation(self, parent1, parent2):
        
        crossover_point = int((len(parent1.chromosome))/2)
        new_chromosome = parent1.chromosome[0:crossover_point] + parent2.chromosome[crossover_point:]
        
        cities_left = [city for city in parent2.chromosome if city not in new_chromosome]
        new_chromosome.extend(cities_left)




        return new_chromosome 



    def chromosome_mutation(self, indexind):
        index1, index2 = random.sample(range(len(indexind.chromosome)), 2)  
        while index1==index2:
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
    cities.draw_cities(city_dict, solver.getBestIndiv().chromosome)
