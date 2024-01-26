import random
from agent import Agent, Creature
from environment import Environment
import os
import time

def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def half_array(array: list) -> list:
    return array[:len(array) // 2]


def mutate_genome(array: list, mutation_rate: float) -> list:
    for i in range(len(array)):
        for j in range(len(array[i])):
            if random.random() <= mutation_rate:
                array[i][j] = random.randint(-1, 1)
    return array

def mutate_internal_layer(array: list, mutation_rate: float) -> list:
    for i in range(len(array)):
        for j in range(len(array[i])):
            if random.random() <= mutation_rate:
                # TODO mutate internal layer
                # internal layer = list of [list, list] where each list[0] is a list of input connections and list[1] is a list of output connections
                # each connection in EACH list should be potentially removed based on mutation rate
                # additonally, mutation rate should dictate creation of new links
                ...
    return array


def reproduce(agent_a: Agent, agent_b: Agent, env: Environment, mutation_rate: float = 0.01) -> None:
    '''
    two lists that need to be concatenated:
     - genome
     - input layer
     ensure that if agent[0] gives (left-half of genome) they give (right-helf of input layer)
     and vice versa

     After reproduction, place child at location of agent_a and add to environment.
     Additionally, apply the mutation rate to each connection between layers.
     Make sure that any reduntant neurons are handled for efficiency
     '''
    if random.choice([0, 1]) == 0:
        left_half_genome = half_array(agent_a.genome)
        right_half_genome = half_array(agent_b.genome)
        left_internal_layer = half_array(agent_b.internal_layer)
        right_internal_layer = half_array(agent_a.internal_layer)
        child_location = agent_a.location
    else:
        left_half_genome = half_array(agent_b.genome)
        right_half_genome = half_array(agent_a.genome)
        left_internal_layer = half_array(agent_a.internal_layer)
        right_internal_layer = half_array(agent_b.internal_layer)
        child_location = agent_b.location
    child_genome = left_half_genome + right_half_genome
    child_internal_layer = left_internal_layer + right_internal_layer
    child_genome = mutate_genome(child_genome, mutation_rate)
    child_internal_layer = mutate_internal_layer(child_internal_layer, mutation_rate)
    child = Creature(child_location, 1, 'F', child_genome, child_internal_layer)
    env.add_agent(child)
    


if __name__ == "__main__":
    reward = 1
    n = 4
    food = 'F'
    env = Environment((10, 10), [])
    starting_indices = env.get_possible_starting_indices(n)
    agents = [Creature(starting_indices[i], reward, food) for i in range(n)]
    env.set_agents(agents)
    env.populate('F', 0.5)
    for i in range(1000):
        clear_terminal()
        print(env)
        time.sleep(0.1)
        for agent in env.living_agents:
            env.move(agent, random.choice(['N', 'E', 'S', 'W']))