import math
import random

class Agent:
    def __init__(self, location: tuple[int, int], fitness: float, target, genome = list[list[int]], internal_layer = list[list[int]],age: int = 0) -> None:
        self.is_alive: bool = True
        self.location: tuple[int, int] = location
        self.fitness: float = fitness
        self.target = target
        self.age: int = age
        self.genome: list[list[int]] = genome
        self.internal_layer: list[list[int]] = internal_layer


    def __hyperbolic_tangent_function(self, x: float) -> float:
        return (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)


    def __can_reproduce(self, other) -> bool:
        return (self.age >= 10 and other.age >= 10) and (self.fitness >= 3 and other.fitness >= 3) and (self.genetic_similarity(other) >= 0.8)


    def genetic_similarity(self, other) -> float:
        '''
        Similarity between genomes (between 0 and 1) + similarity between internal layers (between 0 and 1) / 2
        '''
        genome_similarity = 0
        internal_layer_similarity = 0
        for i in range(len(self.genome)):
            for j in range(len(self.genome[i])):
                if self.genome[i][j] == other.genome[i][j]:
                    genome_similarity += 1
        for i in range(len(self.internal_layer)):
            for j in range(len(self.internal_layer[i])):
                if self.internal_layer[i][j] == other.internal_layer[i][j]:
                    internal_layer_similarity += 1
        genome_similarity /= len(self.genome) * len(self.genome[0])
        internal_layer_similarity /= len(self.internal_layer) * len(self.internal_layer[0])
        return (genome_similarity + internal_layer_similarity) / 2


    def consume(self, target, reward) -> bool:
        if self.target == target:
            self.fitness += reward
            return True
        else:
            return False


    def update_location(self, location: tuple[int, int]) -> None:
        self.location = location
        self.fitness -= 0.1


    def death_check(self) -> bool:
        if self.fitness <= 0:
            self.is_alive = False
            return True
        else:
            return False
        



class Creature(Agent):
    def __init__(self, location: tuple[int, int], fitness: float, target, genome = list[list[int]], internal_layer = list[list[int]], age: int = 0) -> None:
        super().__init__(location, fitness, target, genome, internal_layer, age)

    def __str__(self) -> str:
        return 'C'
    
    def __repr__(self) -> str:
        return 'C'