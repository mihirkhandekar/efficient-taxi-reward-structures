from strategy.greedy_strategy import GreedyStrategy
from strategy.nash_strategy import NashStrategy


class Game:
    def __init__(self, agents, goals, strategy=GreedyStrategy()):
        self.time_grid = []
        self.strategy = strategy
        self.agents = agents
        self.goals = goals
        self.current_utility = 0

    def generate_strategy_over_time(self):
        # Based on self.strategy, calculate cost and utility
        pass

    def visualize(self):
        # Visualize all grids over time T
        pass

    def summary(self):
        # Show total utility and agent-specific utility
        return ('Printing Utility')

def initialize_agents():
    return []

def initialize_goals():
    return []


if __name__ == '__main__':
    agents = initialize_agents()
    goals = initialize_goals()
    greedy_game = Game(agents, goals)
    nash_game = Game(agents, goals)
    epsilon = 0.000001
    print('Greedy Game :' , greedy_game.summary())
    print('Nash Game :' , nash_game.summary())
    print('Price of Anarchy : ', greedy_game.current_utility / (nash_game.current_utility + epsilon))
