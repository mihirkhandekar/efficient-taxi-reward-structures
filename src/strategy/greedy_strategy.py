from strategy.strategy import Strategy
from config import DEBUG, SUPER_DEBUG

class GreedyStrategy(Strategy):
    def get_strategy(self, grid):
        # Uses agents and goals in grid and uses a custom method to return which agent which goal is assigned to.
        agent_assignments = dict()
        agent_assignments_ids = dict()

        agents = grid.agents
        goals = grid.goals
        total_utility = 0
        for agent in agents:
            max_utility = 0
            best_goal = None
            if agent.hidden:
                agent_assignments_ids[agent.id] = None
                agent_assignments[agent] = None

            for goal in goals:
                capacity_utilization = abs(agent.capacity - goal.capacity)
                utility = goal.get_reward(
                    capacity_utilization) - grid.get_total_moving_cost(agent, goal)
                if utility > max_utility:
                    max_utility = utility
                    best_goal = goal
                if SUPER_DEBUG:
                    print('Utility Agent {}, Goal {} = {}'.format(agent.id, goal.id, utility))
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
            
            if max_utility > 0:
                total_utility += max_utility

        if DEBUG:
            print('Agent-Goal assignments : ', agent_assignments_ids)

        return agent_assignments, max_utility
