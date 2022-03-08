from turtle import back
import numpy as np
import pygame
import random
import time

class Q_Learning:
    # Do Q_Learning

    alpha = 0.01
    gamma = 0.9
    current_pos = [0, 0]
    epsilon = 0.25
    actions = {"up": 0,"down" : 1,"left" : 2,"right" : 3} #possible actions

    def __init__(self, x_pos, y_pos):
        screen = pygame.display.set_mode( (x_pos*100, y_pos*100) )

        run = True
        while run:
            # Setting Map as White
            screen.fill( (0, 0, 0) )

            # Visualize Map 
            Q_Learning.Visual_Map(screen, x_pos, y_pos)

            # Listening events
            for event in pygame.event.get():
                # If you push exit button in game => Game will quit
                if event.type == pygame.QUIT:
                    run = False
            
            # Update display
            pygame.display.flip()

            # Switching Positions
            Q_Learning.Steps(x_pos, y_pos)
        
        # Pygame fin
        pygame.quit()

    def Visual_Map(screen, x_pos, y_pos):
        '''
        Visualize Map as n x n
        Still Editing 
        '''
        c = 0
        for i in range(0,x_pos*100,100):
            for j in range(0,y_pos*100,100):
                pygame.draw.rect(screen,(50,50,50),(j,i,j+100,i+100),0)
                pygame.draw.rect(screen,Learning_Environments.colors[c],(j+3,i+3,j+95,i+95),0)
                c+=1
                pygame.draw.circle(screen,(25,129,230),(Q_Learning.current_pos[1]*100 + 50,Q_Learning.current_pos[0]*100 + 50),30,0)        

    def Select_Action(current_state, x_pos, y_pos):
        '''
        Making Possible actions basis of current position.
        '''

        # Initialize possible actions
        possible_actions = []

        # If random uniform [0, 1] le epsilon
        if np.random.uniform() <= Q_Learning.epsilon:

            # Setting up, down, left, right consider of walls position.
            if Q_Learning.current_pos[0] != 0 and [Q_Learning.current_pos[0]-1,Q_Learning.current_pos[1]] not in Learning_Environments.walls:
                possible_actions.append("up")
            if Q_Learning.current_pos[0] != x_pos-1 and [Q_Learning.current_pos[0]+1, Q_Learning.current_pos[1]] not in Learning_Environments.walls:
                possible_actions.append("down")
            if Q_Learning.current_pos[1] != 0 and [Q_Learning.current_pos[0],Q_Learning.current_pos[1]-1] not in Learning_Environments.walls:
                possible_actions.append("left")
            if Q_Learning.current_pos[1] != y_pos-1 and [Q_Learning.current_pos[0],Q_Learning.current_pos[1]+1] not in Learning_Environments.walls:
                possible_actions.append("right")
            action = Q_Learning.actions[possible_actions[random.randint(0,len(possible_actions) - 1)]]
        else:

            # Get min value at current_states
            m = np.min(Learning_Environments.q_table[current_state])
            # Setting up, down, left, right consider of walls position.
            if Q_Learning.current_pos[0] != 0 and [Q_Learning.current_pos[0]-1,Q_Learning.current_pos[1]] not in Learning_Environments.walls: #up
                possible_actions.append(Learning_Environments.q_table[current_state,0])
            else:
                possible_actions.append(m - 100)
            if Q_Learning.current_pos[0] != x_pos-1 and [Q_Learning.current_pos[0]+1, Q_Learning.current_pos[1]] not in Learning_Environments.walls: #down
                possible_actions.append(Learning_Environments.q_table[current_state,1])
            else:
                possible_actions.append(m - 100)
            if Q_Learning.current_pos[1] != 0 and [Q_Learning.current_pos[0],Q_Learning.current_pos[1]-1] not in Learning_Environments.walls: #left
                possible_actions.append(Learning_Environments.q_table[current_state,2])
            else:
                possible_actions.append(m - 100)
            if Q_Learning.current_pos[1] != y_pos-1 and [Q_Learning.current_pos[0],Q_Learning.current_pos[1]+1] not in Learning_Environments.walls: #right
                possible_actions.append(Learning_Environments.q_table[current_state,3])
            else:
                possible_actions.append(m - 100)
            
            #Random choice using value
            action = random.choice([i for i,a in enumerate(possible_actions) if a == max(possible_actions)]) #randomly selecting one of all possible actions with maximin value
        return action
        
        
    def Steps(x_pos, y_pos):
        '''
        Do steps per action
        '''

        # Get current states
        current_state = Learning_Environments.states[(Q_Learning.current_pos[0],Q_Learning.current_pos[1])]

        # Get action
        action = Q_Learning.Select_Action(current_state, x_pos, y_pos)

        # Calculate after position
        if action == 0: #move up
            Q_Learning.current_pos[0] -= 1
        elif action == 1: #move down
            Q_Learning.current_pos[0] += 1
        elif action == 2: #move left
            Q_Learning.current_pos[1] -= 1
        elif action == 3: #move right
            Q_Learning.current_pos[1] += 1
        new_state = Learning_Environments.states[(Q_Learning.current_pos[0],Q_Learning.current_pos[1])]

        # If new_state is not in terminals 
        if new_state not in Learning_Environments.terminals:
            # Calculate rewards
            Learning_Environments.q_table[current_state,action] += Q_Learning.alpha*(Learning_Environments.reward[Q_Learning.current_pos[0],Q_Learning.current_pos[1]] + Q_Learning.gamma*(np.max(Learning_Environments.q_table[new_state])) - Learning_Environments.q_table[current_state,action])
        else:
            Learning_Environments.q_table[current_state,action] += Q_Learning.alpha*(Learning_Environments.reward[Q_Learning.current_pos[0],Q_Learning.current_pos[1]] - Learning_Environments.q_table[current_state,action])
            Q_Learning.current_pos = [0,0]
            if Q_Learning.epsilon > 0.05:
                Q_Learning.epsilon -= 3e-4 #reducing as time increases to satisfy Exploration & Exploitation Tradeoff

class Learning_Environments:

    # Initialize Reward, it means total map scores
    reward = np
    colors = np

    # Initialize Walls
    walls = []

    # Initialize Terminal, Terminal means zero in Q-learning
    terminals = []

    # Initialize states
    states = {}
    states_queue=0

    # Initialize Q-table
    q_table = np

    def __init__(self, x_pos, y_pos):
        # Initialize Colors => x_pos * y_pos 
        Learning_Environments.colors = [(255, 255, 255) for i in range(x_pos*y_pos)]

        # Set Reward Scores, Walls, Penalties        
        Learning_Environments.Set_Reward(x_pos, y_pos)

        # Set States at each Position
        Learning_Environments.Set_State(x_pos, y_pos)     

        # Set Terminals
        Learning_Environments.terminals.append(x_pos*y_pos - 1)

        # Initialize q_table
        Learning_Environments.q_table = np.zeros( (x_pos * y_pos, 4))

    def Set_Reward(x_pos, y_pos):
        '''
        Set Rewards
        Input
        - x position, y position

        Output
        - goals, penalties, walls
        '''

        # Initialize reward as Zero
        Learning_Environments.reward = np.zeros( (x_pos,y_pos) )

        # Set two Walls, Penalties
        for idx in range(2):
            Learning_Environments.Set_Penalty(x_pos, y_pos)
            Learning_Environments.Set_Wall(x_pos, y_pos)

        # Set Goals
        Learning_Environments.reward[x_pos-1, y_pos-1] = 1
        Learning_Environments.colors[x_pos * y_pos - 1] = (0, 255, 0)

    def Set_Penalty(x_pos, y_pos):
        # Randomize some number
        rand_x_pos = random.randint(0, x_pos-1)
        rand_y_pos = random.randint(0, y_pos-1)

        if Learning_Environments.reward[rand_x_pos, rand_y_pos] == 0 and [rand_x_pos, rand_y_pos] != ([0, 0] or [x_pos-1, y_pos-1]):
            # Set Penalty as -1
            Learning_Environments.reward[rand_x_pos, rand_y_pos] = -1
            Learning_Environments.colors[rand_x_pos * y_pos + rand_y_pos] = (255, 0, 0)

    def Set_Wall(x_pos, y_pos):
        # Randomize some number
        rand_x_pos = random.randint(0, x_pos-1)
        rand_y_pos = random.randint(0, y_pos-1)

        if Learning_Environments.reward[rand_x_pos, rand_y_pos] == 0 and [rand_x_pos, rand_y_pos] != ([0, 0] or [x_pos-1, y_pos-1]):
            # Set Penalty as -255
            Learning_Environments.walls.append([rand_x_pos, rand_y_pos])
            Learning_Environments.colors[rand_x_pos * y_pos + rand_y_pos] = (0, 0, 255)

    def Set_State(x_pos, y_pos):

        # Set State Queue as x, y positions
        '''
        Example.
        1 (0,0), 2 (0,0), 3 (0,0)
        4 (0,0), 5 (0,0), 6 (0,0)
        7 (0,0), 8 (0,0), 9 (0,0)
        '''
        [ [ [Learning_Environments.Set_Queue(Learning_Environments.states, i, j)] for j in range(y_pos)] for i in range(x_pos)]

    def Set_Queue(states, i, j):
        states[(i, j)] = Learning_Environments.states_queue
        Learning_Environments.states_queue += 1

class Do_Maze:

    def __init__(self, x_pos, y_pos):
        Learning_Environments(x_pos, y_pos)
        Q_Learning(x_pos, y_pos)

if __name__ == "__main__":
    Do_Maze(10, 10)

