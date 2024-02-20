import mastermind as mm
import random







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
        """ Initialize the population with pop_size random Individuals """
        # We ititialize an array for the population and create new individuals in this array according to the population size
        # we stock in chromosome a random allocation of colors thanks to the mastermind function where colors are defined and 
        #randomly assigned and in fitness we calculate the score of the allocation. 

        self._population = []
        for _ in range(pop_size): 
            chromosome = MATCH.generate_random_guess() 
            fitness = MATCH.rate_guess(chromosome) 
            self._population.append(Individual(chromosome, fitness)) 

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
        survivors = self._population[:int(len(self._population) * self._selection_rate)]
        while len(self._population) < len(survivors): # here we take two random parent from the survivor and calculate the new
            # chromosome by taking a part of the first parent and a part of the second parent. 
            # The crossoverpoint is here to decide what part we take from each parent. le 1er parent prend la partie avant le crossover point et le deuxième sa partie après le crossoverpoint
            parent1, parent2 = random.sample(survivors, 2)
            crossover_point = random.randint(1, len(parent1.chromosome) - 1)
            new_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
            if random.random() < self._mutation_rate: #in the case where the random number is inferior to mutation rate we change the color of an random index with a random color
                mutation_index = random.randint(0, len(new_chromosome) - 1)
                new_chromosome[mutation_index] = random.choice(mm.get_possible_colors)
            new_fitness = MATCH.rate_guess(new_chromosome)
            self._population.append(Individual(new_chromosome, new_fitness)) 



    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        for individual in self._population: 
            print(individual)

    def get_best_individual(self): #scan through all the individuals and take the one with max fitness score. 
        """ Return the best Individual of the population """
        return max(self._population, key=lambda indiv: indiv.fitness)

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        for _ in range(max_nb_of_generations): # here we iterate the evolve generation function until it reach the max or if the fitness score reach the treshold ie. the perfect score
            self.evolve_for_one_generation()
            if threshold_fitness and self.get_best_individual().fitness >= threshold_fitness:
                break



MATCH = mm.MastermindMatch(secret_size=4)
solver = GASolver()
solver.reset_population()
solver.evolve_until(threshold_fitness=MATCH.max_score())

best = solver.get_best_individual()
print(f"Best guess {best.chromosome}")
print(f"Problem solved? {MATCH.is_correct(best.chromosome)}")
