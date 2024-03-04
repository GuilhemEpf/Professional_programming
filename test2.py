import cities
import random


class Individual:
    def __init__(self, chromosome: list, fitness: float):
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GASolver:
    def __init__(self, selection_rate=0.5, mutation_rate=0.05):
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50, city_dict=None):
        """ Initialize the population with pop_size random Individuals 

        Args:
            pop_size (integer): Number of individuals in the population.
            city_dict (dict): Dictionary containing city information. 
        """
        if city_dict is None:
            raise ValueError("City dictionary is required for initializing the population.")
        
        for i in range(pop_size):
            chromosome = cities.default_road(city_dict)
            random.shuffle(chromosome)
            fitness = -cities.road_length(city_dict, chromosome)
            new_individual = Individual(chromosome, fitness)
            self._population.append(new_individual)

    def evolve_for_one_generation(self, city_dict):
        self._population.sort(reverse=True)

        # Selection: Remove x% of the population (less adapted)
        x = 50
        x_percent_index = int(len(self._population) * x / 100)
        self._population = self._population[:int(-x_percent_index)]

        # Reproduction: Recreate the same quantity by crossing the surviving ones
        new_chromosomes = []

        for i in range(len(self._population)):
            parent1 = random.choice(self._population)
            parent2 = random.choice(self._population)

            while parent2 == parent1:
                parent2 = random.choice(self._population)

            crossover_point = len(parent1.chromosome) // 2
            new_chrom = parent1.chromosome[0:crossover_point] + parent2.chromosome[crossover_point:]

            unique_list = []
            for item in new_chrom:
                if item not in unique_list:
                    unique_list.append(item)
            new_chrom = unique_list

            while len(new_chrom) != len(parent1.chromosome):
                possible_cities = cities.default_road(city_dict)
                new_gene = random.choice(possible_cities)
                while new_gene in new_chrom:
                    new_gene = random.choice(possible_cities)
                new_chrom.append(new_gene)

            p = self._mutation_rate
            number = random.random()

            if number < p:
                pos1 = random.randint(0, len(new_chrom) - 1)
                pos2 = random.randint(0, len(new_chrom) - 1)

                while pos2 == pos1:
                    pos2 = random.randint(0, len(new_chrom) - 1)

                new_chrom[pos1], new_chrom[pos2] = new_chrom[pos2], new_chrom[pos1]

            new_individual = Individual(new_chrom, -cities.road_length(city_dict, new_chrom))
            new_chromosomes.append(new_individual)

        self._population = self._population + new_chromosomes

    def show_generation_summary(self):
        for individual in self._population:
            print(individual)

    def get_best_individual(self):
        results = self._population
        results.sort(key=lambda x: x.fitness, reverse=True)
        print(results[0])
        return results[0]

    def evolve_until(self, max_nb_of_generations=500, city_dict=None):
        for i in range(0, max_nb_of_generations):
            self.evolve_for_one_generation(city_dict)


city_dict = cities.load_cities("cities.txt")
solver = GASolver()
solver.reset_population(city_dict=city_dict)
solver.evolve_until(city_dict=city_dict)

best = solver.get_best_individual()
cities.draw_cities(city_dict, best.chromosome)
