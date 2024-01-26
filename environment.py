from agent import Agent, Creature
import random

class Environment:
    def __init__(self, size: tuple[int, int], agents: list[Agent]) -> None:
        self.size: tuple[int, int] = size
        self.map: list[list[int]] = [[[] for _ in range(size[0])] for _ in range(size[1])]
        self.all_agents: list[Agent] = []
        self.living_agents: list[Agent] = []
        self.set_agents(agents)


    def set_agents(self, agents: list[Agent]):
        '''
        Warning: Hard Sets the agents in the environment.
        Will override any existing agents.
        '''
        self.all_agents = agents
        self.living_agents = agents
        for agent in self.living_agents:
            if self.__is_agent(agent.location):
                raise Exception('Agent location already occupied')
            else:
                self.map[agent.location[0]][agent.location[1]].append(agent)
        self.population: int = len(self.living_agents)


    def add_agent(self, new_agent: Agent) -> None:
        if new_agent.is_alive:
            self.all_agents.append(new_agent)
            self.living_agents.append(new_agent)
            self.map[new_agent.location[0]][new_agent.location[1]].append(new_agent)
            self.update_population()
        else:
            self.all_agents.append(new_agent)


    def __str__(self) -> str:
        max_array = max([len(str("".join(str(self.map[y][x])))) for x in range(self.size[0]) for y in range(self.size[1])])
        return "\n".join([" ".join([str("".join(str(self.map[y][x])).ljust(max_array)) for x in range(self.size[0])]) for y in range(self.size[1])])
    

    def get_possible_starting_indices(self, n) -> list[tuple[int, int]]:
        indices = []
        while len(indices) < n:
            index = (random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1))
            if not self.__is_agent(index):
                indices.append(index)
        return indices


    def populate(self, item, frequency: float) -> bool:
        '''
        Populates the environment with a given item at a given frequency.
        - Generates n random indices
        - if the index is empty, populates it with the given item
        - else, generate a new index until n is reached
        '''
        n = int(self.size[0] * self.size[1] * frequency)
        indices = [(random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)) for _ in range(n)]
        for index in indices:
            if not item in self.map[index[0]][index[1]]:
                self.map[index[0]][index[1]].append(item)
            else:
                while item in self.map[index[0]][index[1]]:
                    index = (random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1))
                self.map[index[0]][index[1]].append(item)
        return True
    

    def move(self, agent: Agent, direction: str) -> bool:
        if direction not in ['N', 'E', 'S', 'W']:
            return False
        else:
            if direction == 'N':
                new_location = (agent.location[0] - 1, agent.location[1])
            elif direction == 'S':
                new_location = (agent.location[0] + 1, agent.location[1])
            elif direction == 'E':
                new_location = (agent.location[0], agent.location[1] + 1)
            elif direction == 'W':
                new_location = (agent.location[0], agent.location[1] - 1)
            if self.__in_bounds(new_location):
                if not self.__is_agent(new_location):
                    self.__remove_agent(agent.location)
                    self.map[new_location[0]][new_location[1]].append(agent)
                    agent.update_location(new_location)
                    return True
                else:
                    return False
            else:
                return False
            

    def get_neighbour(self, location: tuple[int, int], direction: str) -> Agent | None:
        '''
        Returns agent obj in the given direction if exists
        '''
        if direction not in ['N', 'E', 'S', 'W']:
            return None
        else:
            if direction == 'N':
                new_location = (location[0] - 1, location[1])
            elif direction == 'S':
                new_location = (location[0] + 1, location[1])
            elif direction == 'E':
                new_location = (location[0], location[1] + 1)
            elif direction == 'W':
                new_location = (location[0], location[1] - 1)
            if self.__in_bounds(new_location):
                if self.__is_agent(new_location):
                    for item in self.map[new_location[0]][new_location[1]]:
                        if isinstance(item, Agent):
                            return item
                else:
                    return None
            else:
                return None


    def consume(self, location: tuple[int, int]) -> bool:
        '''
        Removes non-agent items from the environment
        '''
        self.map[location[0]][location[1]] = [item for item in self.map[location[0]][location[1]] if isinstance(item, Agent)]
        return True


    def update_population(self) -> None:
        self.population = len(self.living_agents)


    def __in_bounds(self, location: tuple[int, int]) -> bool:
        return 0 <= location[0] < self.size[0] and 0 <= location[1] < self.size[1]


    def __is_empty(self, location: tuple[int, int]) -> bool:
        return len(self.map[location[0]][location[1]]) == 0


    def has_target(self, location: tuple[int, int, int], agent: Agent) -> bool:
        return agent.target in self.map[location[0]][location[1]]


    def __remove_agent(self, location: tuple[int, int]) -> bool:
        for i in range(len(self.map[location[0]][location[1]])):
            if isinstance(self.map[location[0]][location[1]][i], Agent):
                self.map[location[0]][location[1]].pop(i)
                return True
        return False


    def __is_agent(self, location: tuple[int, int]) -> bool:
        if self.__in_bounds(location):
            return any(isinstance(item, Agent) for item in self.map[location[0]][location[1]])
        else:
            return False

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # INPUT SENSORY METHODS
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def FAT(self, agent: Agent) -> float:
        '''
        Food at target
        -1 if no food at target, 1 if food at target
        '''
        return 1 if self.has_target(agent.location, agent) else -1
    
    def FDF(self, agent: Agent) -> float:
        '''
        Food density forward. 
        '''
        column = []
        i = 0
        while i < agent.location[0]:
            column.append(self.map[i][agent.location[1]])
            i += 1
        return len([item for sublist in column for item in sublist if agent.target in sublist]) / agent.location[0]

    def FDR(self, agent: Agent) -> float:
        '''
        Food density right.
        '''
        row = []
        i = agent.location[1]
        while i < self.size[1]:
            row.append(self.map[agent.location[0]][i])
            i += 1
        return len([item for sublist in row for item in sublist if agent.target in sublist]) / (self.size[1] - agent.location[1])
    
    def FDL(self, agent: Agent) -> float:
        '''
        Food density left.
        '''
        row = []
        i = 0
        while i < agent.location[1]:
            row.append(self.map[agent.location[0]][i])
            i += 1
        return len([item for sublist in row for item in sublist if agent.target in sublist]) / agent.location[1]
    
    def FDB(self, agent: Agent) -> float:
        '''
        Food density backward.
        '''
        column = []
        i = agent.location[0]
        while i < self.size[0]:
            column.append(self.map[i][agent.location[1]])
            i += 1
        return len([item for sublist in column for item in sublist if agent.target in sublist]) / (self.size[0] - agent.location[0])
    
    def CLF(self, agent: Agent) -> float:
        '''
        Creature left
        '''
        left = (agent.location[0], agent.location[1] - 1)
        return 1 if self.__is_agent(left) else -1
    
    def CLR(self, agent: Agent) -> float:
        '''
        Creature right
        '''
        right = (agent.location[0], agent.location[1] + 1)
        return 1 if self.__is_agent(right) else -1
    
    def CFD(self, agent: Agent) -> float:
        '''
        Creature forward
        '''
        forward = (agent.location[0] - 1, agent.location[1])
        return 1 if self.__is_agent(forward) else -1
    
    def CBD(self, agent: Agent) -> float:
        '''
        Creature backward
        '''
        backward = (agent.location[0] + 1, agent.location[1])
        return 1 if self.__is_agent(backward) else -1
    
    def PLF(self, agent: Agent) -> float:
        '''
        Population density left
        '''
        row = []
        i = 0
        while i < agent.location[1]:
            row.append(self.map[agent.location[0]][i])
            i += 1
        return len([item for sublist in row for item in sublist if isinstance(item, Agent)]) / agent.location[1]
    
    def PRT(self, agent: Agent) -> float:
        '''
        Population density right
        '''
        row = []
        i = agent.location[1]
        while i < self.size[1]:
            row.append(self.map[agent.location[0]][i])
            i += 1
        return len([item for sublist in row for item in sublist if isinstance(item, Agent)]) / (self.size[1] - agent.location[1])
    
    def PFD(self, agent: Agent) -> float:
        '''
        Population density forward
        '''
        column = []
        i = 0
        while i < agent.location[0]:
            column.append(self.map[i][agent.location[1]])
            i += 1
        return len([item for sublist in column for item in sublist if isinstance(item, Agent)]) / agent.location[0]
    
    def PBD(self, agent: Agent) -> float:
        '''
        Population density backward
        '''
        column = []
        i = agent.location[0]
        while i < self.size[0]:
            column.append(self.map[i][agent.location[1]])
            i += 1
        return len([item for sublist in column for item in sublist if isinstance(item, Agent)]) / (self.size[0] - agent.location[0])
    
    def BDY(self, agent: Agent) -> float:
        '''
        north-south border distance
        normalised between 0 and 1
        '''
        return agent.location[0] / self.size[0]
    
    def BDX(self, agent: Agent) -> float:
        '''
        east-west border distance
        normalised between 0 and 1
        '''
        return agent.location[1] / self.size[1]
    
    def BD(self, agent: Agent) -> float:
        '''
        nearest border distance
        normalised between 0 and 1
        '''
        return min(agent.location[0] / self.size[0], agent.location[1] / self.size[1])
    

    # INPUT HANDLER
    def request_handle(self, sensory_id: int, agent: Agent) -> float:
        '''
        This takes a data request from the agent and returns the appropriate function float
        This is from the functions specified above, namely:
        0: Fat = food at location *
        1: Fdf = food density forward * 
        2: Fdr = food density right *
        3: Fdl = food density left *
        4: Fdb = food density backward *
        8: Clf = creature left *
        9: Clr = creature right *
        10: Cfd = creature forward * 
        11: Cbd = creature backward *
        12: Plf = population density left *
        13: Prt = population density right *
        14: Pfd = population density forward *
        15: Pbd = population density backward *
        18: BDy = north/south border distance *
        19: BDx = east/west border distance *
        20: BD = nearest border distance *
        21, 22, 23, 24 = get_neighbour:
            21 = 'N' -> north
            22 = 'S' -> south
            23 = 'W' -> west
            24 = 'E' -> east
        '''
        if sensory_id == 0:
            return self.FAT(agent)
        elif sensory_id == 1:
            return self.FDF(agent)
        elif sensory_id == 2:
            return self.FDR(agent)
        elif sensory_id == 3:
            return self.FDL(agent)
        elif sensory_id == 4:
            return self.FDB(agent)
        elif sensory_id == 8:
            return self.CLF(agent)
        elif sensory_id == 9:
            return self.CLR(agent)
        elif sensory_id == 10:
            return self.CFD(agent)
        elif sensory_id == 11:
            return self.CBD(agent)
        elif sensory_id == 12:
            return self.PLF(agent)
        elif sensory_id == 13:
            return self.PRT(agent)
        elif sensory_id == 14:
            return self.PFD(agent)
        elif sensory_id == 15:
            return self.PBD(agent)
        elif sensory_id == 18:
            return self.BDY(agent)
        elif sensory_id == 19:
            return self.BDX(agent)
        elif sensory_id == 20:
            return self.BD(agent)
        elif sensory_id == 21:
            return self.get_neighbour(agent.location, 'N')
        elif sensory_id == 22:
            return self.get_neighbour(agent.location, 'S')
        elif sensory_id == 23:
            return self.get_neighbour(agent.location, 'W')
        elif sensory_id == 24:
            return self.get_neighbour(agent.location, 'E')
        else:
            return 0