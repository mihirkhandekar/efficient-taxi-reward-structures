from strategy.strategy import Strategy

class GreedyStrategy(Strategy):
    def get_strategy(self, grid):
        # Uses agents and goals in grid and uses a custom method to return which agent which goal is assigned to.
        agent_assignments = dict()
        init_agents = grid.agents
        goals = grid.goals
        ag = dict()
        for agent in init_agents:
            max_utility = 0
            best_goal = None
            # agent.print()
            for goal in goals:
                capacity_utilization = abs(agent.capacity - goal.capacity)
                utility = goal.get_reward(capacity_utilization) - grid.get_total_moving_cost(agent, goal)
                if utility > max_utility:
                    max_utility = utility
                    best_goal = goal 
            if best_goal != None:
                agent_assignments[agent] = best_goal
                ag[agent.id] = best_goal.id
        print('Strategy : ', ag)

        return agent_assignments
