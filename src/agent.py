class Agent:
    def __init__(self, pos_x, pos_y, id = 0, capacity=5, cur_cost = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.capacity = capacity
        self.cur_cost = cur_cost
        self.id = id            #TODO : Global control of ID assignment
    
    def move(self, pos_x, pos_y, cur_cost = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cur_cost = cur_cost
