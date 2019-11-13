import numpy as np

from strategy.strategy import Strategy
from config import DEBUG, SUPER_DEBUG

class GreedyStrategy(Strategy):
    def get_strategy(self, grid):
        # Uses agents and goals in grid and uses a custom method to return which agent which goal is assigned to.
        agent_assignments = dict()
        agent_assignments_ids = dict()

        agents = grid.agents
        goals = grid.goals

        for agent in agents:
            min_cost = np.inf
            best_goal = None

            for goal in goals:
                cost = grid.get_total_moving_cost(agent, goal)
                if cost < min_cost:
                    min_cost = cost
                    best_goal = goal
                if SUPER_DEBUG:
                    print('Cost Agent {}, Goal {} = {}'.format(agent.summary(), goal.summary(), cost))

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
