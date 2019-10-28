from agent import Agent
from goal import Goal
import math
import matplotlib.pyplot as plt
import numpy as np


# TODO : Improve method documentation
class Grid:
    def __init__(self, time=0, grid_height=25, grid_width=25, agents=[], goals=[]):
        #TODO : Validate initial positions of agents and goals
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.__add_default_ids(agents, goals)
        self.agents = agents
        self.goals = goals
        self.time = time

    def __add_default_ids(self, agents, goals):
        index = 0
        blank_agents = sum([agent.id == None for agent in agents])
        blank_goals = sum([goal.id == None for goal in goals])
        if blank_agents > 0:
            for agent in agents:
                agent.id = index
                index += 1
        index = 0
        if blank_goals > 0:
            for goal in goals:
                goal.id = index
                index += 1


    def move(self, agents, directions, goals):
        '''
            Move list of [agents] in [directions] to [goals]
        '''
        self.__validate_move(agents, directions, goals)

        # Call __get_cost method for agent and direction. Update cur_cost for agent, increments time and return new_grid
        # TODO : Validate if action valid at that position

        new_agents = self.__update_agent_position_and_cost(agents, directions, goals)

        self.__merge_new_agent_positions_with_existing(new_agents)

        new_grid = Grid(self.time + 1, self.grid_height,
                        self.grid_width, new_agents, self.goals)
        return new_grid

    def __get_cost(self, agent, direction):
        # This method gets cost for agent to move 1 step in a direction
        # Typically equal for all directions = 1
        return 1

    def __merge_new_agent_positions_with_existing(self, new_agents):
        modified_positions = [new_agent.id for new_agent in new_agents]
        for agent in self.agents:
            if agent.id not in modified_positions:
                new_agents.append(agent)
                modified_positions.append(agent.id)

    def __update_agent_position_and_cost(self, agents, directions, goals):
        new_agents = []

        for agent, direction, goal in zip(agents, directions, goals):
            if agent.hide:
                agent.decrement_hide()
                continue

            self.update_agent_at_goal_state(agent, goal, goals)

            if 'UP' in direction:
                agent.pos_x += 1
            if 'DOWN' in direction:
                agent.pos_x -= 1
            if 'LEFT' in direction:
                agent.pos_y -= 1
            if 'RIGHT' in direction:
                agent.pos_y += 1
            if direction != 'STAY':
                agent.cur_cost += self.__get_cost(agent, direction)

            new_agents.append(agent)
            return new_agents

    def update_agent_at_goal_state(self, agent, goal, goals):
        # TODO : Rewrite this complex logic. If agent at goal state, stays hidden and reappears randomly. 
        if agent.pos_x == goal.pos_x and agent.pos_y == goal.pos_y:
            capacity_utilization = abs(agent.capacity - goal.capacity)
            agent.cur_filled_capacity = capacity_utilization

            agent.decrement_hide()
            agent.hide = True

            if capacity_utilization >= goal.capacity:
                goals.remove(goal)
            else:
                goal.capacity -= capacity_utilization

    def __validate_move(self, agents, directions, goals):
        if len(agents) != len(directions) or len(agents) != len(goals):
            raise ValueError(
                'Number of agents should be equal to number of directions')

        # TODO : Use enum for directions
        for direction in directions:
            if direction not in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UP_LEFT', 'UP_RIGHT', 'DOWN_LEFT', 'DOWN_RIGHT', 'STAY']:
                raise ValueError('Invalid direction ', direction)

        for agent, direction in zip(agents, directions):
            if (agent.pos_x == 0 and 'DOWN' in direction) or (agent.pos_y == 0 and 'LEFT' in direction) or (agent.pos_x == self.grid_height - 1 and 'UP' in direction) or (agent.pos_y == self.grid_width - 1 and 'RIGHT' in direction):
                raise ValueError(
                    '{} is an invalid value for agent {}'.format(direction, agent))

    def get_total_moving_cost(self, agent, goal):
        # Get cost to move agent from its current position to passed goal
        x_diff = abs(agent.pos_x - goal.pos_x)
        y_diff = abs(agent.pos_y - goal.pos_y) 
        cost = abs(x_diff - y_diff) + min(x_diff, y_diff)
        return cost

    def visualize(self):
        # Visualizes current grid
        l_x=[]
        l_y=[]
        g_x=[]
        g_y=[]
        numGoals=len(goals)
        numAgents=len(agents)

        for agent in agents:
            l_x.append(agent.pos_x)
            l_y.append(agent.pos_y)
        for goal in goals:
            g_x.append(goal.pos_x)
            g_y.append(goal.pos_y)
        alabels=[]
        glabels=[]
        
        gloc=[]
        for i in range(numGoals):
            gloc.append((g_x[i],g_y[i]))
        aloc=[]
        for i in range(numAgents):
            aloc.append((l_x[i],l_y[i]))
        gloc_s = set(gloc)
        aloc_s = set(aloc)
        acount=[]
        gcount=[]
        for i in range(len(gloc_s)):
            gcount.append(gloc.count(list(gloc_s)[i])*5)
        for i in range(len(aloc_s)):
            acount.append(aloc.count(list(aloc_s)[i])*5)
        loc_s=gloc_s.union(aloc_s)

        gloc_x=[]
        gloc_y=[]
        aloc_x=[]
        aloc_y=[]

        gloc_s=list(gloc_s)
        aloc_s=list(aloc_s)
        for i in gloc_s:
            gloc_x.append(i[0])
            gloc_y.append(i[1])
        for i in aloc_s:
            aloc_x.append(i[0])
            aloc_y.append(i[1])


        for i in aloc_s:
            lab_a=""
            
            for j in range(len(aloc)):
                if i==aloc[j]:
                    lab_a+="A"
                    lab_a+=str(j)
                    lab_a+=","
            alabels.append(lab_a)
        for i in gloc_s:
            
            lab_g=""
            for j in range(len(gloc)):
                if i == gloc[j]:
                    lab_g+="G"
                    lab_g+=str(j)
                    lab_g+=","
            if i in aloc_s:
                lab_g+=alabels[aloc_s.index(i)]
            glabels.append(lab_g)


        
        names=np.array(alabels)
        names1=np.array(glabels)
        fig, ax=plt.subplots()
        sc = plt.scatter(aloc_x,aloc_y,c='red',s=acount)
        sc1 = plt.scatter(gloc_x,gloc_y,c='blue',s=gcount)
        annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",bbox=dict(boxstyle="round", fc="w"),arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(ind):

            pos = sc.get_offsets()[ind["ind"][0]]
            annot.xy = pos
            '''
            text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                                " ".join([names[n] for n in ind["ind"]]))
            '''
            text = "Goals/Agents: {}".format(" ".join([names[n] for n in ind["ind"]]))
            #----------
            
            annot.set_text(text)
            #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
            annot.get_bbox_patch().set_alpha(0.4)

        def update_annot1(ind):

            pos = sc1.get_offsets()[ind["ind"][0]]
            annot.xy = pos
            '''
            text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                                " ".join([names[n] for n in ind["ind"]]))
            '''
            text = "Goals/Agents: {}".format(" ".join([names1[n] for n in ind["ind"]]))
            #----------
            
            annot.set_text(text)
            #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
            annot.get_bbox_patch().set_alpha(0.4)
        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                cont, ind = sc.contains(event)
                if cont:
                    update_annot(ind)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()
                cont, ind = sc1.contains(event)
                if cont:
                    update_annot1(ind)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)
                
        plt.title('Location of Agents and Goals')
        plt.xticks(range(n))
        plt.yticks(range(n))
        plt.grid()
        plt.legend(loc=2)
        plt.show()

def print(self):
    print('Agents: ')
    [agent.print() for agent in self.agents]
    print('Goals: ')
    [goal.print() for goal in self.goals]

if __name__ == '__main__':
    # Test this class
    agent1 = Agent(pos_x = 0, pos_y = 0, capacity=10)
    agent2 = Agent(pos_x = 1, pos_y = 3, capacity=10)
    goal1 = Goal(pos_x = 5, pos_y = 5, capacity=10)
    goal2 = Goal(pos_x = 5, pos_y = 5, capacity=10)

    grid = Grid(agents=[agent1, agent2], goals=[goal1, goal2])
    print('Initial grid')
    grid.print()
    grid = grid.move([agent1], ['UP'], [goal1])
    print('Final grid')
    grid.print()

