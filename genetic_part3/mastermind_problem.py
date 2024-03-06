# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import GAProblem
import mastermind as mm
MATCH = mm.MastermindMatch(secret_size=6)  
import random

class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem"""
   
    def chromosome(self):
        chromosome=MATCH.generate_random_guess()

        return chromosome
    def fitness(self, chromosome): 
        fitness=MATCH.rate_guess(chromosome)
        return fitness    


    def evolve_generation(self, parent1, parent2, ):
        crossover_point = random.randrange(0, len(parent1.chromosome))
        new_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
        return new_chromosome
        
    def chromosome_mutation(self, population,indexind):
        mutation_index = random.randint(0, len(indexind.chromosome) - 1)
   
        new_chromosome = indexind.chromosome[0:mutation_index] + [random.choice(mm.get_possible_colors())] + indexind.chromosome[mutation_index+1:] 
        
        return new_chromosome       
        

if __name__ == '__main__':

    from ga_solver import GASolver

    MATCH = mm.MastermindMatch(secret_size=6)
    problem = MastermindProblem(MATCH)
    solver = GASolver(problem)

    solver.reset_population()
    solver.evolve_until()

    print(
        f"Best guess {mm.decode_guess(solver.getBestDNA())} {solver.get_best_individual()}")
    print(
        f"Problem solved? {MATCH.is_correct(solver.get_best_individual().chromosome)}")
