import numpy as np
import copy
import itertools

class CentralPlanner():
    def get_strategy(self, grid):
        agents = grid.agents
        goals = grid.goals
        print(grid.summary())
        goal_permutations = itertools.permutations(goals)
        agent_permutations = itertools.permutations(agents)
        #print('Permutations', [permutation for permutation in permutations])

        distances = []
        for goal_permutation in goal_permutations:
            distances.extend(
                self.get_moving_distance(
                    copy.deepcopy(agent_permutation),
                    copy.deepcopy(goal_permutation),
                )
                for agent_permutation in agent_permutations
            )

        print('DISTANCES', distances)
        return np.min(distances)

    def get_moving_distance(self, agents, goals):
        distance = 0
        new_agents = []
        new_goals = []

        for agent, goal in zip(agents, goals):
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

        if new_agents and new_goals:
            goal_permutations = itertools.permutations(new_goals)
            agent_permutations = itertools.permutations(new_agents)
            min_dist = np.inf
            for goal_permutation in goal_permutations:
                for agent_permutation in agent_permutations:
                    dist = self.get_moving_distance(copy.deepcopy(agent_permutation), copy.deepcopy(goal_permutation))
                    if dist < min_dist:
                        min_dist = dist
            return distance + min_dist
        return distance


    def get_total_moving_cost(self, agent, goal):
        x_diff = abs(agent.pos_x - goal.pos_x)
        y_diff = abs(agent.pos_y - goal.pos_y)
        return max(x_diff, y_diff)
