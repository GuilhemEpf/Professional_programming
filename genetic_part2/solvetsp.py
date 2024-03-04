import cities
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
    def __init__(self, selection_rate=0.5, mutation_rate=0.05):
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
        city_dict = cities.load_cities("C:/Users/guilh/OneDrive/Bureau/A4/Professional Programming/TP3/Professional_programming/genetic_part2/cities.txt")

        for _ in range(pop_size):
            chromosome = cities.default_road(city_dict)
            random.shuffle(chromosome)
            fitness = -cities.road_length(city_dict, chromosome)
            new_individual = Individual(chromosome, fitness)
            self._population.append(new_individual)

    def evolve_for_one_generation(self,city_dict):
        """ Apply the process for one generation:
            - Sort the population (Descending order)
            - Selection: Remove x% of population (less adapted)
            - Reproduction: Recreate the same quantity by crossing the surviving ones
            - Mutation: For each new Individual, mutate with probability mutation_rate
        """
        self._population.sort(reverse=True)  # Sort the population in descending order

        poptodelete = len(self._population) * 0.5  # Proportion of population kept
        self._population = self._population[:int(-poptodelete)]

        new_added_indiv = []
        for i in range(len(self._population)):
            parent1 = random.choice(self._population)
            parent2 = random.choice(self._population)
            while parent2 == parent1:
                parent2 = random.choice(self._population)

            crossover_point = int((len(parent1.chromosome))/2)
            new_chromosome = parent1.chromosome[0:crossover_point] + parent2.chromosome[crossover_point:]
            
            remaining_cities = [city for city in parent2.chromosome if city not in new_chromosome]
            new_chromosome.extend(remaining_cities)
            new_fitness = -cities.road_length(city_dict, new_chromosome)
            new_individual = Individual(new_chromosome, new_fitness)
            new_added_indiv.append(new_individual)

        self._population = self._population + new_added_indiv

        for indexind in self._population:
            if len(self._population) != 50:
                if random.random() < self._mutation_rate:
                    index1, index2 = random.sample(range(len(indexind.chromosome)), 2)  
                    while index1==index2:
                        index2=random.randint(0,len(new_chromosome)-1)
                        new_chromosome[index1],new_chromosome[index2] = new_chromosome[index2],new_chromosome[index1]
                    new_chromosome = indexind.chromosome.copy()
                    new_chromosome[index1], new_chromosome[index2] = new_chromosome[index2], new_chromosome[index1]
                    new_fitness = -cities.road_length(city_dict, new_chromosome)
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
        """ Launch the evolve_for_one_generation function until one of the two conditions is achieved:
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to threshold_fitness
        """
        for _ in range(0,max_nb_of_generations):
            self.evolve_for_one_generation(city_dict)


city_dict = cities.load_cities("C:/Users/guilh/OneDrive/Bureau/A4/Professional Programming/TP3/Professional_programming/genetic_part2/cities.txt")
solver = GASolver()
solver.reset_population()
solver.evolve_until()

best = solver.get_best_individual()
cities.draw_cities(city_dict, best.chromosome)
