from Population import Population
from GeneticAgent import GeneticAgent

class GeneticPlatform:
    def __init__(self, pop_size):
        self.generation = Population(pop_size)
        self.generation_no = 0
    
    def progress_gen(self):
        print("Generation: {}".format(self.generation_no))
        print("Generation size: {}".format(self.generation.size))
        next_gen = Population(0)
        
        while next_gen.size < self.generation.size:
            offspring = self.generation.create_offspring()
            next_gen.add_member(offspring)
            next_gen.add_member(offspring.copy().mutate(0.3))
            next_gen.add_member(offspring.copy().mutate(1))
            
        self.generation = next_gen
        
