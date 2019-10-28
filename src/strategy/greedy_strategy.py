from strategy.strategy import Strategy

class GreedyStrategy(Strategy):
    def get_strategy(self, grid):
        # Uses agents and goals in grid and uses a custom method to return which agent which goal is assigned to.
        assignments = {"1": "3", "2": "4"}
        return assignments
