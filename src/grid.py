# TODO : Improve method documentation
class Grid:
    def __init__(self, time=0, grid_height=25, grid_width=25, agents=[], goals=[]):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.agents = agents
        self.goals = goals
        self.time = time

    def __get_cost(self, agent, direction):
        # This method gets cost for agent to move 1 step in a direction
        # Typically equal for all directions = 1
        pass

    def move(self, agents, directions):
        '''
            Move list of [agents] in [directions]
        '''
        if len(agents) != len(directions):
            raise ValueError(
                'Number of agents should be equal to number of directions')

        for direction in directions:
            if direction not in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UL', 'UR', 'DL', 'DR']:
                raise Exception('Invalid direction')
        # Call __get_cost method for agent and direction. Update cur_cost for agent, increments time and return new_grid
        # TODO : Validate if action valid at that position
        new_grid = Grid()
        return new_grid

    def get_total_moving_cost(self, agent, goal):
        # Get cost to move agent from its current position to passed goal
        pass

    def visualize(self):
        # Visualizes current grid
        pass