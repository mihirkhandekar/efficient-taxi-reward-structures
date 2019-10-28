from strategy.strategy import Strategy

class GreedyStrategy(Strategy):
    def get_strategy(self, grid):
        # Uses agents and goals in grid and uses a custom method to return which agent which goal is assigned to.
        goal_assignments = dict()
        init_agents = grid.agents
        goals = grid.goals

        for agent in init_agents:
            max_utility = 0
            best_goal = None
            for goal in goals:
                if not agent.hide and goal not in goal_assignments:
                    capacity_utilization = abs(agent.capacity - goal.capacity)
                    utility = goal.get_reward(capacity_utilization) - grid.get_total_moving_cost(agent, goal)
                    if utility > max_utility:
                        max_utility = utility
                        best_goal = goal 
            goal_assignments[best_goal] = agent

        return goal_assignments
