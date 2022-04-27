class Agent:
    HIDE = 5
    def __init__(self, pos_x, pos_y, id = None, capacity=5, cur_utility = 0, cur_filled_capacity = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.capacity = capacity
        self.cur_utility = cur_utility
        self.id = id            #TODO : Global control of ID assignment
        self.cur_filled_capacity = cur_filled_capacity
        self.cur_distance = 0
        self.hide_timeout = self.HIDE
        self.hidden = False
    
    def move(self, pos_x, pos_y, cur_utility = 0):
        # TODO : Currently not being called. Need to call
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cur_utility = cur_utility
    
    def decrement_hide(self):
        reappear = True
        self.hide_timeout -= 1
        if self.hide_timeout == 0:
            self.reset_hide()
            return reappear
        return ~reappear
    
    def reset_hide(self):
        self.hide_timeout = self.HIDE
        self.cur_filled_capacity = 0
        self.hidden = False
    

    def summary(self):
        return f'Agent {self.id} at ({self.pos_x}, {self.pos_y}) : Cap {self.cur_filled_capacity}/{self.capacity} : Current Utility {self.cur_utility} '