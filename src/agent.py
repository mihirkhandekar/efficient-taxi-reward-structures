class Agent:
    def __init__(self, pos_x, pos_y, id = 0, capacity=5, cur_cost = 0, cur_filled_capacity = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.capacity = capacity
        self.cur_cost = cur_cost
        self.id = id            #TODO : Global control of ID assignment
        self.cur_filled_capacity = cur_filled_capacity
    
    def move(self, pos_x, pos_y, cur_cost = 0):
        # TODO : Currently not being called. Need to call
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cur_cost = cur_cost

    def print(self):
        print('Agent {} at ({}, {}) : Cap {}/{} : Current Cost {}'.format(self.id, self.pos_x, self.pos_y, self.cur_filled_capacity, self.capacity, self.cur_cost))