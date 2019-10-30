import numpy as np
from strategy.greedy_strategy import GreedyStrategy
from strategy.nash_strategy import NashStrategy
from agent import Agent
from goal import Goal
from grid import Grid
import copy
from config import DEBUG, SUPER_DEBUG, GRID_WIDTH, GRID_HEIGHT

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
        self.time_grid = [copy.copy(init_grid)]
        self.strategy = strategy
        self.current_utility = 0

    def generate_strategy_over_time(self):
        time = 0
        grid = copy.copy(self.init_grid)
        grid.visualize()

        print('Time :', time)
        print('Grid :', grid.summary())
        
        while(len(grid.goals) > 0 and time < TIMEOUT):
            agent_assignments, utility = self.strategy.get_strategy(grid)
            self.current_utility += utility
            move_directions = []
            move_agents = []
            move_goals = []
            
            for agent, goal in agent_assignments.items():
                if goal != None:
                    if agent.pos_x < goal.pos_x and agent.pos_y < goal.pos_y:
                        move_directions.append('UP_RIGHT')
                    elif agent.pos_x < goal.pos_x and agent.pos_y > goal.pos_y:
                        move_directions.append('UP_LEFT')
                    elif agent.pos_x > goal.pos_x and agent.pos_y > goal.pos_y:
                        move_directions.append('DOWN_LEFT')
                    elif agent.pos_x > goal.pos_x and agent.pos_y < goal.pos_y:
                        move_directions.append('DOWN_RIGHT')
                    elif agent.pos_x > goal.pos_x and agent.pos_y == goal.pos_y:
                        move_directions.append('DOWN')
                    elif agent.pos_x < goal.pos_x and agent.pos_y == goal.pos_y:
                        move_directions.append('UP')
                    elif agent.pos_x == goal.pos_x and agent.pos_y > goal.pos_y:
                        move_directions.append('LEFT')
                    elif agent.pos_x == goal.pos_x and agent.pos_y < goal.pos_y:
                        move_directions.append('RIGHT')
                    else:
                        move_directions.append('STAY')
                    move_agents.append(agent)
                    move_goals.append(goal)
                
                else:
                    move_directions.append('STAY')
                    move_agents.append(agent)
                    move_goals.append(goal)
                
                if SUPER_DEBUG:
                    print('Agent {} to move {}'.format(move_agents[-1].id, move_directions[-1]))

            grid = grid.move(move_agents, move_directions, move_goals)
            self.time_grid.append(copy.copy(grid))

            time += 1
            print('Time :', time)
            print('Grid :', grid.summary())
            grid.visualize()

        print('Stopping all agents with {} goals and {}/{} time. Agent can now think of other career options.'.format(len(grid.goals), time, TIMEOUT))


    def visualize(self):
        # Visualize all grids over time T
        for tgrid in greedy_game.time_grid:
            tgrid.visualize()

    def summary(self):
        # Show total utility and agent-specific utility
        grids = []
        for tgrid in greedy_game.time_grid:
            grids.append(tgrid.summary())
        return grids


def initialize_agents():
    np.random.seed(SEED_AGENT)
    agents = []
    for i in range(INITIAL_AGENTS):
        pos_x = np.random.randint(0, GRID_HEIGHT)
        pos_y = np.random.randint(0, GRID_WIDTH)
        agent = Agent(pos_x, pos_y, id=i, capacity=np.random.randint(1, MAX_AGENT_CAPACITY))
        agents.append(agent)
    return agents

def initialize_goals():
    np.random.seed(SEED_GOAL)
    goals = []
    for i in range(INITIAL_GOALS):
        pos_x = np.random.randint(0, GRID_HEIGHT)
        pos_y = np.random.randint(0, GRID_WIDTH)
        goal = Goal(pos_x, pos_y, id=i, capacity=np.random.randint(1, MAX_GOAL_CAPACITY))
        goals.append(goal)
    return goals

def initialize_grid(init_agents, goals):
    return Grid(grid_height=GRID_HEIGHT, grid_width=GRID_WIDTH, agents=init_agents, goals=goals)
    

if __name__ == '__main__':
    # Initialize agents and goals randomly
    init_agents = initialize_agents()
    goals = initialize_goals()

    # Initialize grid with agents and goals
    init_grid = initialize_grid(init_agents, goals)
    
    # Greedy game
    greedy_game = Game(init_grid, strategy=GreedyStrategy())
    greedy_game.generate_strategy_over_time()

    nash_game = Game(init_grid, strategy=NashStrategy())
    epsilon = 0.000001
    print('Greedy Game utility:' , greedy_game.current_utility)
    
    print('Nash Game utility:' , nash_game.current_utility)
    print('Price of Anarchy : ', greedy_game.current_utility / (nash_game.current_utility + epsilon))
