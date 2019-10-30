import numpy as np
from strategy.greedy_strategy import GreedyStrategy
from strategy.nash_strategy import NashStrategy
from agent import Agent
from goal import Goal
from grid import Grid
import copy

GRID_HEIGHT = 25
GRID_WIDTH = 25
INITIAL_AGENTS = 10
INITIAL_GOALS = 10
MAX_AGENT_CAPACITY = 5
MAX_GOAL_CAPACITY = 5

SEED_AGENT = 7
SEED_GOAL = 8

TIMEOUT = 20


class Game:
    def __init__(self, init_grid, strategy=GreedyStrategy()):
        self.init_grid = init_grid
        self.time_grid = []
        self.strategy = strategy
        self.current_utility = 0

    def generate_strategy_over_time(self):
        time = 0
        grid = self.init_grid
        self.time_grid.append(copy.copy(grid))
        while(len(grid.goals) > 0 and time < TIMEOUT):
            print('Time ', time)
            time += 1
            agent_assignments = self.strategy.get_strategy(grid)
            directions = []
            agents = []
            goals = []
            for agent, goal in agent_assignments.items():
                if goal != None:
                    if agent.pos_x < goal.pos_x and agent.pos_y < goal.pos_y:
                        directions.append('UP_RIGHT')
                    elif agent.pos_x < goal.pos_x and agent.pos_y > goal.pos_y:
                        directions.append('UP_LEFT')
                    elif agent.pos_x > goal.pos_x and agent.pos_y > goal.pos_y:
                        directions.append('DOWN_LEFT')
                    elif agent.pos_x > goal.pos_x and agent.pos_y < goal.pos_y:
                        directions.append('DOWN_RIGHT')
                    elif agent.pos_x > goal.pos_x and agent.pos_y == goal.pos_y:
                        directions.append('DOWN')
                    elif agent.pos_x < goal.pos_x and agent.pos_y == goal.pos_y:
                        directions.append('UP')
                    elif agent.pos_x == goal.pos_x and agent.pos_y > goal.pos_y:
                        directions.append('LEFT')
                    elif agent.pos_x == goal.pos_x and agent.pos_y < goal.pos_y:
                        directions.append('RIGHT')
                    else:
                        directions.append('STAY')
                    agents.append(agent)
                    goals.append(goal)
            print('Moving {} agents'.format(len(agents)))
            grid = grid.move(agents, directions, goals)
            print('Grid : ', grid.print())
            self.time_grid.append(copy.copy(grid))

    def visualize(self):
        # Visualize all grids over time T
        for tgrid in greedy_game.time_grid:
            tgrid.visualize()

    def summary(self):
        # Show total utility and agent-specific utility
        for tgrid in greedy_game.time_grid:
            pass #tgrid.print()

def initialize_agents():
    np.random.seed(SEED_AGENT)
    agents = []
    for _ in range(INITIAL_AGENTS):
        pos_x = np.random.randint(0, GRID_HEIGHT)
        pos_y = np.random.randint(0, GRID_WIDTH)
        agent = Agent(pos_x, pos_y, capacity=np.random.randint(1, MAX_AGENT_CAPACITY))
        agents.append(agent)
    return agents

def initialize_goals():
    np.random.seed(SEED_GOAL)
    goals = []
    for _ in range(INITIAL_GOALS):
        pos_x = np.random.randint(0, GRID_HEIGHT)
        pos_y = np.random.randint(0, GRID_WIDTH)
        goal = Goal(pos_x, pos_y, capacity=np.random.randint(1, MAX_GOAL_CAPACITY))
        goals.append(goal)
    return goals

def initialize_grid(init_agents, goals):
    return Grid(grid_height=GRID_HEIGHT, grid_width=GRID_WIDTH, agents=init_agents, goals=goals)
    

if __name__ == '__main__':
    init_agents = initialize_agents()
    goals = initialize_goals()
    init_grid = initialize_grid(init_agents, goals)
    greedy_game = Game(init_grid, strategy=GreedyStrategy())
    greedy_game.generate_strategy_over_time()

    nash_game = Game(init_grid, strategy=NashStrategy())
    epsilon = 0.000001
    print('Greedy Game :' , greedy_game.summary())
    greedy_game.visualize()
    print('Nash Game :' , nash_game.summary())
    print('Price of Anarchy : ', greedy_game.current_utility / (nash_game.current_utility + epsilon))
