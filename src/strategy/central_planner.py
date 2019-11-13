import numpy as np
import copy
import itertools

class CentralPlanner():
    def get_strategy(self, grid):
        agents = grid.agents
        goals = grid.goals
        print(grid.summary())
        permutations = itertools.permutations(goals)
        #print('Permutations', [permutation for permutation in permutations])
        distances = []
        for permutation in permutations:
            print('++++')
            distances.append(self.get_moving_distance(copy.deepcopy(agents), copy.deepcopy(permutation)))
        print('DISTANCES', distances)
        return np.min(distances)

    def get_moving_distance(self, agents, goals):
        distance = 0
        new_agents = []
        new_goals = []

        for agent, goal in zip(agents, goals):
            print('+cost ', self.get_total_moving_cost(agent, goal))
            distance += self.get_total_moving_cost(agent, goal)
            agent_seats = agent.capacity-agent.cur_filled_capacity
            if agent_seats == goal.capacity:
                continue
            elif agent_seats > goal.capacity:
                goal.capacity = 0
                agent.cur_filled_capacity = goal.capacity
                agent.pos_x = goal.pos_x
                agent.pos_y = goal.pos_y
                new_agents.append(agent)
            elif agent_seats < goal.capacity:
                goal.capacity -= agent_seats
                new_goals.append(goal)

        if len(new_agents) > 0 and len(new_goals) > 0:
            permutations = itertools.permutations(new_goals)
            min_dist = np.inf
            for permutation in permutations:
                dist = self.get_moving_distance(copy.deepcopy(agents), copy.deepcopy(permutation))
                if dist < min_dist:
                    min_dist = dist
            return distance + min_dist
        return distance


    def get_total_moving_cost(self, agent, goal):
        x_diff = abs(agent.pos_x - goal.pos_x)
        y_diff = abs(agent.pos_y - goal.pos_y) 
        cost = max(x_diff, y_diff)
        return cost
