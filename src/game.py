import numpy as np
from strategy.greedy_strategy import GreedyStrategy
from strategy.opt_strategy import OptStrategy
from agent import Agent
from goal import Goal
from grid import Grid
import copy
from config import DEBUG, SUPER_DEBUG, GRID_WIDTH, GRID_HEIGHT

INITIAL_AGENTS = 10
INITIAL_GOALS = 10
MAX_AGENT_CAPACITY = 10
MAX_GOAL_CAPACITY = 10

SEED_AGENT = None
SEED_GOAL = None

TIMEOUT = 100

class Game:
    def __init__(self, i_grid, strategy=GreedyStrategy()):
        self.init_grid = copy.deepcopy(i_grid)
        self.time_grid = [copy.deepcopy(i_grid)]
        self.strategy = strategy
        self.current_utility = 0

    def generate_strategy_over_time(self):
        time = 0
        grid = copy.deepcopy(self.init_grid)
        grid.visualize()

        print('Time :', time)
        print('Grid :', grid.summary())

        
        while(len(grid.goals) > 0 and len(grid.agents) > 0 and time < TIMEOUT):
            agent_assignments = self.strategy.get_strategy(grid)

            move_directions = []
            move_agents = []
            move_goals = []
            
            self.__extract_move_directions_from_strategy(agent_assignments, move_directions, move_agents, move_goals)

            if all(direction=='STAY' for direction in move_directions):
                break

            grid = grid.move(move_agents, move_directions, move_goals)
            self.time_grid.append(copy.deepcopy(grid))

            time += 1
            print('Time :', time)
            print('Grid :', grid.summary())
            grid.visualize()

        print('Stopping all agents with {} goals and {}/{} time. Agent can now think of other career options.'.format(len(grid.goals), time, TIMEOUT))
        return time

    def __extract_move_directions_from_strategy(self, agent_assignments, move_directions, move_agents, move_goals):
        for agent, goal in agent_assignments.items():
            if goal != None:
                if agent.pos_x < goal.pos_x and agent.pos_y < goal.pos_y:
                    move_directions.append('UP_RIGHT')
                elif agent.pos_x < goal.pos_x and agent.pos_y > goal.pos_y:
                    move_directions.append('UP_LEFT')
                elif agent.pos_x > goal.pos_x and agent.pos_y > goal.pos_y and agent.pos_x > 0 and agent.pos_y > 0:
                    move_directions.append('DOWN_LEFT')
                elif agent.pos_x > goal.pos_x and agent.pos_y < goal.pos_y and agent.pos_x > 0:
                    move_directions.append('DOWN_RIGHT')
                elif agent.pos_x > goal.pos_x and agent.pos_y == goal.pos_y and agent.pos_x > 0:
                    move_directions.append('DOWN')
                elif agent.pos_x < goal.pos_x and agent.pos_y == goal.pos_y:
                    move_directions.append('UP')
                elif agent.pos_x == goal.pos_x and agent.pos_y > goal.pos_y and agent.pos_y > 0:
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


    def visualize(self):
        # Visualize all grids over time T
        for tgrid in self.time_grid:
            tgrid.visualize()

    def summary(self):
        # Show total utility and agent-specific utility
        
        grids = []
        for tgrid in self.time_grid:
            grids.append(tgrid.summary())
        return self.current_utility, grids


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
    
def get_agents_utility(game):
    grid = game.time_grid[-1]
    agents = grid.agents
    print([agent.cur_utility for agent in agents])
    return np.sum(np.array([agent.cur_utility for agent in agents]))

def get_agents_distance(game):
    grid = game.time_grid[-1]
    agents = grid.agents
    print([agent.cur_distance for agent in agents])
    return np.sum(np.array([agent.cur_distance for agent in agents]))



def get_goals_pending_cap(game):
    grid = game.time_grid[-1]
    goals = grid.goals
    return np.sum(np.array([goal.capacity for goal in goals]))


def simulate():
    init_agents = initialize_agents()
    goals = initialize_goals()

    init_grid = initialize_grid(init_agents, goals)

    print(init_grid.summary())
    
    # Greedy game
    greedy_game = Game(init_grid, strategy=GreedyStrategy())
    print('---------------------', greedy_game.summary())
    greedy_time = greedy_game.generate_strategy_over_time()

    nash_game = Game(init_grid, strategy=OptStrategy())
    print('---------------------', nash_game.summary())
    nash_time = nash_game.generate_strategy_over_time()
    epsilon = 0.000001

    
    print('Greedy Game social cost:' , get_agents_utility(greedy_game), greedy_time, get_goals_pending_cap(greedy_game), get_agents_distance(greedy_game))
    
    print('Nash Game social cost:' , get_agents_utility(nash_game), nash_time, get_goals_pending_cap(nash_game), get_agents_distance(nash_game))

    poa = get_agents_utility(greedy_game) / (get_agents_utility(nash_game) + epsilon)

    timediff = greedy_time/nash_time

    print('Price of Anarchy : ', poa)
    return poa, timediff, get_agents_distance(greedy_game)/get_agents_distance(nash_game)



if __name__ == '__main__':
    # Initialize agents and goals randomly
    poas = []
    times = []
    distdiffs = []
    for i in range(20):
        poa, timediff, distdiff = simulate()
        poas.append(poa)
        times.append(timediff)
        distdiffs.append(distdiff)
    print('POAS', poas)
    print("AVERAGE POA", np.average(np.array(poas)))
    print('TIMES', times)
    print("AVERAGE TIME", np.average(np.array(times)))
    print('DISTS', distdiffs)
    print("AVERAGE DIST", np.average(np.array(distdiffs)))

