from agent import Agent
from goal import Goal
import math

# TODO : Improve method documentation
class Grid:
    def __init__(self, time=0, grid_height=25, grid_width=25, agents=[], goals=[]):
        #TODO : Validate initial positions of agents and goals
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.__add_default_ids(agents, goals)
        self.agents = agents
        self.goals = goals
        self.time = time

    def __add_default_ids(self, agents, goals):
        index = 0
        blank_agents = sum([agent.id == None for agent in agents])
        blank_goals = sum([goal.id == None for goal in goals])
        if blank_agents > 0:
            for agent in agents:
                agent.id = index
                index += 1
        index = 0
        if blank_goals > 0:
            for goal in goals:
                goal.id = index
                index += 1


    def move(self, agents, directions):
        '''
            Move list of [agents] in [directions]
        '''
        self.__validate_move(agents, directions)

        # Call __get_cost method for agent and direction. Update cur_cost for agent, increments time and return new_grid
        # TODO : Validate if action valid at that position

        new_agents = self.__update_agent_position_and_cost(agents, directions)

        self.__merge_new_agent_positions_with_existing(new_agents)

        new_grid = Grid(self.time + 1, self.grid_height,
                        self.grid_width, new_agents, self.goals)
        return new_grid

    def __get_cost(self, agent, direction):
        # This method gets cost for agent to move 1 step in a direction
        # Typically equal for all directions = 1
        return 1

    def __merge_new_agent_positions_with_existing(self, new_agents):
        modified_positions = [new_agent.id for new_agent in new_agents]
        for agent in self.agents:
            if agent.id not in modified_positions:
                new_agents.append(agent)
                modified_positions.append(agent.id)

    def __update_agent_position_and_cost(self, agents, directions):
        new_agents = []

        for agent, direction in zip(agents, directions):
            if 'UP' in direction:
                agent.pos_x += 1
            if 'DOWN' in direction:
                agent.pos_x -= 1
            if 'LEFT' in direction:
                agent.pos_y -= 1
            if 'RIGHT' in direction:
                agent.pos_y += 1

            agent.cur_cost += self.__get_cost(agent, direction)

            new_agents.append(agent)
            return new_agents

    def __validate_move(self, agents, directions):
        if len(agents) != len(directions):
            raise ValueError(
                'Number of agents should be equal to number of directions')

        # TODO : Use enum for directions
        for direction in directions:
            if direction not in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UP_LEFT', 'UP_RIGHT', 'DOWN_LEFT', 'DOWN_RIGHT']:
                raise ValueError('Invalid direction')

        for agent, direction in zip(agents, directions):
            if (agent.pos_x == 0 and 'DOWN' in direction) or (agent.pos_y == 0 and 'LEFT' in direction) or (agent.pos_x == self.grid_height - 1 and 'UP' in direction) or (agent.pos_y == self.grid_width - 1 and 'RIGHT' in direction):
                raise ValueError(
                    '{} is an invalid value for agent {}'.format(direction, agent))

    def get_total_moving_cost(self, agent, goal):
        # Get cost to move agent from its current position to passed goal
        x_diff = abs(agent.pos_x - goal.pos_x)
        y_diff = abs(agent.pos_y - goal.pos_y) 
        cost = abs(x_diff - y_diff) + min(x_diff, y_diff)
        return cost

    def visualize(self):
        # Visualizes current grid
        pass

    def print(self):
        print('Agents: ')
        [agent.print() for agent in self.agents]
        print('Goals: ')
        [goal.print() for goal in self.goals]

if __name__ == '__main__':
    # Test this class
    agent1 = Agent(pos_x = 0, pos_y = 0, capacity=10)
    agent2 = Agent(pos_x = 1, pos_y = 3, capacity=10)
    goal = Goal(pos_x = 5, pos_y = 5, capacity=10)

    grid = Grid(agents=[agent1, agent2], goals=[goal])
    print('Initial grid')
    grid.print()
    grid = grid.move([agent1], ['UP'])
    print('Final grid')
    grid.print()

