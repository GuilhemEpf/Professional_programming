
import random
import cities



class Individual:
    def __init__(self, chromosome: list, fitness: float):
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        return f'Indiv({self.fitness:.1f},{self.chromosome})'

class GASolver:
 

    def reset_population(self, pop_size=50):  #we put a huge population size to get more chance to make sure that we will find the best travel
        """ Initialize the population with pop_size random Individuals 
        
        Args:
            pop_size (integer): number of individuals in the population. 
        """
        for i in range (pop_size):
            chromosome = cities.default_road(city_dict)  #using cities.load_cities, we are able to read the text file summarizing the locations of the cities
            random.shuffle(chromosome)  # works inplace 
            fitness = - cities.road_length(city_dict, chromosome) 
            new_individual = Individual(chromosome, fitness)
            self._population.append(new_individual) 


    def evolve_for_one_generation(self):

        self._population.sort(reverse=True)

        #-	Selection: Remove x% of population (less adapted)
        x = 50  #if we want to remove x purcent of the population
        x_purcent_index = len(self._population) * x / 100  #we calculate the amount of values in the population list to have those x purcent
        self._population = self._population[:int(-x_purcent_index)] #we erase from x_purcent_index to the end of our list

        #-   Reproduction: Recreate the same quantity by crossing the surviving ones 
        new_chromosomes=[] #new_chromosomes which contains all of the children chromosomes
       
        print(len(self._population))
        for i in range(len(self._population)):
        
            parent1 = random.choice(self._population)
            parent2 = random.choice(self._population)

            while parent2==parent1:
                parent2 = random.choice(self._population)
            
            crossing_point = int((len(parent1.chromosome))/2)
            new_chrom = parent1.chromosome[0:crossing_point] + parent2.chromosome[crossing_point:]

            unique_list = []
            for item in new_chrom:
                if item not in unique_list:
                    unique_list.append(item)
            new_chrom=unique_list
  
            
            while len(new_chrom)!=len(parent1.chromosome):
                possible_cities = cities.default_road(city_dict) 
                new_gene = random.choice(possible_cities)
                while new_gene in new_chrom:
                    new_gene = random.choice(possible_cities)
                new_chrom.append(new_gene)

            p = self._mutation_rate  #we chose 0.1 as a probability default value
            number=random.random()
            if number < p:  #if the random number is under the probability, then we take the action, if not, nothing happens
                pos1 = random.randint(0,len(new_chrom)-1)
                pos2=random.randint(0,len(new_chrom)-1)
                while pos2==pos1:
                    pos2=random.randint(0,len(new_chrom)-1)
                    new_chrom[pos1],new_chrom[pos2] = new_chrom[pos2],new_chrom[pos1]
            
            new_individual = Individual(new_chrom, - cities.road_length(city_dict, new_chrom)) # Create a new individual with the given chromosome combination and calculate its fitness
            
        new_chromosomes.append(new_individual)  
        self._population=self._population + new_chromosomes 
        print(len(self._population))

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self): 
        """ Return the best Individual of the population """
        results=[]
        
        results = self._population 
        results.sort(key=lambda x: x.fitness, reverse=True) #Decreasing Order compared to the fitness values.
        print(results[0]) 
        return results[0]

    def evolve_until(self, max_nb_of_generations=500):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        max_nb_of_generations=max_nb_of_generations
        for i in range (0,max_nb_of_generations):
            self.evolve_for_one_generation()  #we take the score for this population
            # if score==threshold_fitness:
            #     break   #if we have the best score, we stop 

city_dict = cities.load_cities("/Users/theoverdelhan/Downloads/GA_GIMOND_LECORNEC-main/Part 2/cities.txt") #using cities.load_cities, we are able to read the text file summarizing the locations of the cities
# print(city_dict)


# city_dict = cities.load_cities("cities.txt") 
solver = GASolver() 
solver.reset_population() 
solver.evolve_until() 

best = solver.get_best_individual() 
cities.draw_cities(city_dict, best.chromosome) 