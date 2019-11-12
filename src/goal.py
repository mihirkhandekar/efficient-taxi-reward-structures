import numpy as np

class Goal:
    
    MEDIAN_DISTANCE = 10
    UNIT_REWARD = 3.0

    def __init__(self, pos_x, pos_y, id = None, capacity=5, cur_cost = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.capacity = capacity
        self.id = id            #TODO : Global control of ID assignment
    
    def get_reward(self, units):
        # Return reward, which is a function of capacity
        # Assuming average distance of Singapore travels with unit reward of UNIT_REWARD per unit. Consider with MEDIAN_DISTANCE as median in normal distribution
        # distance = np.random.normal(loc=self.MEDIAN_DISTANCE, scale=2, size=units)
        
        distance = np.array([10. for i in range(units)])
        return int(np.sum(self.UNIT_REWARD * distance))

    def summary(self):
        return ('Goal {} at ({}, {}) : Cap {}'.format(self.id, self.pos_x, self.pos_y, self.capacity))

if __name__ == '__main__':
    goal = Goal(0, 0, 0)
    print(goal.get_reward(4))