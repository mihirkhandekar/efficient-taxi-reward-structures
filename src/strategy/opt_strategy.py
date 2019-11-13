import numpy as np

from strategy.strategy import Strategy
from config import DEBUG, SUPER_DEBUG, CAPACITY_PENALTY_FACTOR


class OptStrategy(Strategy):
    CAPACITY_PENALTY_FACTOR = CAPACITY_PENALTY_FACTOR
    
    def get_capacity_penalty(self, agent_capacity, goal_capacity):
        return self.CAPACITY_PENALTY_FACTOR * abs(agent_capacity - goal_capacity) / (goal_capacity)


    def get_strategy(self, grid):
        agent_assignments = dict()
        agent_assignments_ids = dict()

        agents = grid.agents
        goals = grid.goals
        for agent in agents:
            max_utility = 0#-np.inf
            best_goal = None
            if agent.hidden:
                agent_assignments_ids[agent.id] = None
                agent_assignments[agent] = None

            for goal in goals:
                capacity_utilization = min(agent.capacity - agent.cur_filled_capacity, goal.capacity)
                utility = goal.get_reward(
                    capacity_utilization) - grid.get_total_moving_cost(agent, goal) - self.get_capacity_penalty(agent.capacity - agent.cur_filled_capacity, goal.capacity)
                if utility > max_utility:
                    max_utility = utility
                    best_goal = goal
                if SUPER_DEBUG:
                    print('Utility Agent {}, Goal {} = {}'.format(agent.summary(), goal.summary(), utility))
            if best_goal != None:
                agent_assignments[agent] = best_goal
                agent_assignments_ids[agent.id] = best_goal.id
                if SUPER_DEBUG:
                    print('Best utility for agent {} in goal {}'.format(agent.id, best_goal.id))
            else:
                agent_assignments_ids[agent.id] = None
                agent_assignments[agent] = None
                if SUPER_DEBUG:
                    print('All goals negative for agent {}. Agent has nowhere to go now. '.format(agent.id))

        if DEBUG:
            print('Agent-Goal assignments : ', agent_assignments_ids)

        return agent_assignments
