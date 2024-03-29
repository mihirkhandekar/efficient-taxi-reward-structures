from agent import Agent
from goal import Goal
from config import GRID_HEIGHT, GRID_WIDTH, DEBUG
from strategy.central_planner import CentralPlanner

import math
import matplotlib.pyplot as plt
import numpy as np
import copy


# TODO : Improve method documentation
class Grid:
    STEP_COST = 2
    def __init__(self, time=0, grid_height=25, grid_width=25, agents=[], goals=[]):
        #TODO : Validate initial positions of agents and goals
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.agents = agents
        self.goals = goals
        self.time = time


    def move(self, agents, directions, goals):
        '''
            Move list of [agents] in [directions] to [goals]
        '''
        self.__validate_move(agents, directions, goals)

        # Call __get_cost method for agent and direction. Update cur_cost for agent, increments time and return new_grid
        # TODO : Validate if action valid at that position

        new_agents, updated_goals = self.__update_agent_position_and_cost(agents, directions, goals)

        self.__update_goals(updated_goals, goals)

        self.__merge_new_agent_positions_with_existing(new_agents)

        return Grid(
            self.time + 1,
            self.grid_height,
            self.grid_width,
            new_agents,
            self.goals,
        )

    def __update_goals(self, updated_goals, goals):
        for updated_goal, capacity in updated_goals.items():
            if capacity is None or capacity <= 0:
                for goal in self.goals:
                    if goal.id == updated_goal.id:
                        self.goals.remove(goal)
            else:
                for goal in self.goals:
                    if goal.id == updated_goal.id:
                        goal.capacity = capacity

    def __get_cost(self, agent, direction):
        # This method gets cost for agent to move 1 step in a direction
        # Typically equal for all directions = 1
        return self.STEP_COST

    def __merge_new_agent_positions_with_existing(self, new_agents):
        modified_positions = [new_agent.id for new_agent in new_agents]
        full_agents = [new_agent.id for new_agent in new_agents if new_agent.capacity == new_agent.cur_filled_capacity]
        
        for agent in self.agents:
            if agent.id not in modified_positions:
                new_agents.append(agent)
                modified_positions.append(agent.id)

    def __update_agent_position_and_cost(self, agents, directions, goals):
        new_agents = []

        all_updated_goals = {}
        for agent, direction, goal in zip(agents, directions, goals):            
            init_position = agent.pos_x, agent.pos_y
            if 'UP' in direction:
                agent.pos_x += 1
            if 'DOWN' in direction:
                agent.pos_x -= 1
            if 'LEFT' in direction:
                agent.pos_y -= 1
            if 'RIGHT' in direction:
                agent.pos_y += 1
            if direction != 'STAY':
                agent.cur_utility -= self.__get_cost(agent, direction)
                agent.cur_distance += 1
            if DEBUG:
                print(
                    f'Agent {agent.id} moved {direction} from {init_position[0]},{init_position[1]} to {agent.pos_x},{agent.pos_y} (dir {direction} cost {agent.cur_utility} +{self.__get_cost(agent, direction)})'
                )


            if goal is not None:
                updated_goals, agent = self.update_agent_at_goal_state(agent, goal, goals)
                all_updated_goals |= updated_goals
            new_agents.append(agent)
        return new_agents, all_updated_goals

    def update_agent_at_goal_state(self, agent, goal, goals):
        # TODO : Rewrite this complex logic. If agent at goal state, stays hidden and reappears randomly. 
        updated_goals = {}
        if agent.pos_x == goal.pos_x and agent.pos_y == goal.pos_y:
            
            capacity_utilization = min(agent.capacity - agent.cur_filled_capacity, goal.capacity)

            agent.cur_filled_capacity = agent.cur_filled_capacity + capacity_utilization

            if DEBUG:
                print(
                    f'Agent {agent.id} ({agent.capacity}) at goal {goal.id} ({goal.capacity})'
                )


            agent.cur_utility += goal.get_reward(capacity_utilization)

            if agent.capacity == agent.cur_filled_capacity:
                agent.hidden = True

            if capacity_utilization == goal.capacity:
                for sgoal in self.goals:
                    if sgoal.id == goal.id:
                        self.goals.remove(sgoal)
                #self.goals.remove(goal)
                updated_goals[goal] = None
            else:
                goal.capacity -= capacity_utilization
                updated_goals[goal] = goal.capacity


        if DEBUG: print('Updating reached goals : ', [updated_goal.summary() for updated_goal in updated_goals])
        return updated_goals, agent

    def __validate_move(self, agents, directions, goals):
        if len(agents) != len(directions) or len(agents) != len(goals):
            raise ValueError(
                'Number of agents should be equal to number of directions and goals')

        # TODO : Use enum for directions
        for direction in directions:
            if direction not in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UP_LEFT', 'UP_RIGHT', 'DOWN_LEFT', 'DOWN_RIGHT', 'STAY']:
                raise ValueError('Invalid direction ', direction)

        for agent, direction in zip(agents, directions):
            if (agent.pos_x == 0 and 'DOWN' in direction) or (agent.pos_y == 0 and 'LEFT' in direction) or (agent.pos_x == self.grid_height - 1 and 'UP' in direction) or (agent.pos_y == self.grid_width - 1 and 'RIGHT' in direction):
                raise ValueError(f'{direction} is an invalid value for agent {agent}')

    def get_total_moving_cost(self, agent, goal):
        # Get cost to move agent from its current position to passed goal
        x_diff = abs(agent.pos_x - goal.pos_x)
        y_diff = abs(agent.pos_y - goal.pos_y) 
        # cost = abs(x_diff - y_diff) + min(x_diff, y_diff)
        cost = max(x_diff, y_diff)
        return self.STEP_COST * cost

    def visualize(self):
        # Visualizes current grid
        
        numGoals=len(self.goals)
        numAgents=len(self.agents)

        alabels=[]
        glabels=[]
        aloc=[]
        gloc=[]

        for agent in self.agents:
            if not agent.hidden:
                aloc.append((agent.pos_x,agent.pos_y))
        for goal in self.goals:
            gloc.append((goal.pos_x,goal.pos_y))
    
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
            
            for agent in self.agents:
                
                if agent.pos_x==i[0] and agent.pos_y==i[1] and agent.hidden==False:
                    
                    lab_a+="A"
                    lab_a+=str(agent.id)
                    lab_a+=","
            alabels.append(lab_a)
        for i in gloc_s:
            
            lab_g=""
            for goal in self.goals:
                if goal.pos_x==i[0] and goal.pos_y==i[1]:
                    
                    lab_g+="G"
                    lab_g+=str(goal.id)
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
            text = f'Goals/Agents: {" ".join([names[n] for n in ind["ind"]])}'
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
            text = f'Goals/Agents: {" ".join([names1[n] for n in ind["ind"]])}'
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
                elif vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
                cont, ind = sc1.contains(event)
                if cont:
                    update_annot1(ind)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                elif vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)
                
        plt.title('Location of Agents and Goals')
        plt.xticks(range(self.grid_width))
        plt.yticks(range(self.grid_height))
        plt.grid()
        plt.legend(loc=2)
        plt.show()

    def summary(self):
        agent_summary = [agent.summary() for agent in self.agents]
        goal_summary = [goal.summary() for goal in self.goals]
        return agent_summary, goal_summary

if __name__ == '__main__':
    # Test this class
    agent1 = Agent(pos_x = 0, pos_y = 0, capacity=10)
    agent2 = Agent(pos_x = 1, pos_y = 3, capacity=10)
    goal1 = Goal(pos_x = 5, pos_y = 5, capacity=10)
    goal2 = Goal(pos_x = 5, pos_y = 5, capacity=10)

    grid = Grid(agents=[agent1, agent2], goals=[goal1, goal2])
    '''    print('Initial grid')
        print(grid.summary())
        grid = grid.move([agent1], ['UP'], [goal1])
        print('Final grid')
        print(grid.summary())
    '''
    central_planner = CentralPlanner()
    central_planner.get_strategy(grid)



