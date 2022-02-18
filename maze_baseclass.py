import numpy as np
import pandas as pd
from itertools import product
from playsound import playsound
import pickle
from random_maze_generator import RMaze
import time
from copy import copy

# goal.mp3 is Creative Common music by Alexander Blu (sped up a little)

class Maze():
    """
    Remark : North and South are exchanged compared to maze-creator rendering and
    compared to the actions in main.
    """

    def __init__(self, size= (6,6), init_pos = (0,0), goal = (6,6)):
        self.size = size
        cells = list(product(np.arange(size[0]),np.arange(size[1])))
        self.maze = pd.DataFrame(columns=['cell', "N", 'S', 'E', 'W'])
        self.maze['cell']=cells
        self.maze['N']=0
        self.maze['S']=0
        self.maze['E']=0
        self.maze['W']=0
        self.current_pos = list(init_pos)
        self.goal = goal

    def get_walls(self):
        return self.maze.loc[self.maze['cell']==tuple(self.current_pos)].values[0]

    def go_1(self, direction):
        if direction == 'down':
            id_d = 2
        elif direction == "up":
            id_d = 1
        elif direction == "left":
            id_d = 3
        else:
            id_d = 4
        walls = self.get_walls()
        if walls[id_d]==1:
            return True
        else:
            if id_d == 2:
                self.current_pos[1] = self.current_pos[1]+1
            elif id_d == 1 :
                self.current_pos[1] = self.current_pos[1]-1
            elif id_d == 3 :
                self.current_pos[0] = self.current_pos[0]-1
            else:
                self.current_pos[0] = self.current_pos[0]+1

            if tuple(self.current_pos) == self.goal:
                playsound('sounds/goal.mp3')

            return False

    def go(self,direction, tilt):
        finished = False
        iter = 0
        old_pos = copy(self.current_pos)
        while not finished:
            finished = self.go_1(direction)
            iter += 1
            if not tilt:
                break
        if (iter > 1) and tilt and not (tuple(self.current_pos) == self.goal):
            self.describe_cell()
        if old_pos == self.current_pos:
            playsound('sounds/Marimba_3_2.wav')

    def describe_cell(self):
        if tuple(self.current_pos) == self.goal:
            playsound('sounds/goal.mp3')
        else:
            walls = self.get_walls()
            for f in [3,1,4,2]:
                if walls[f] == 1:
                    playsound('sounds/Marimba_1_2.wav')
                else:
                    playsound('sounds/Marimba_2_2.wav')
                time.sleep(0.1)
    def where_goal(self):
        if tuple(self.current_pos) == self.goal:
            playsound('sounds/goal.mp3')
        else:
            dist = np.abs(self.current_pos[0]-self.goal[0])+np.abs(self.current_pos[1]-self.goal[1])
            for _ in range(dist):
                playsound('sounds/Marimba_4_2.wav')


    def add_walls(self, walls):
        for cell_1, cell_2 in walls :
            self._add_wall(cell_1, cell_2)

    def _add_wall(self, cell_1, cell_2):

        if cell_1[0] == cell_2[0]:
            if cell_1[1] == cell_2[1] +1 :
                self.maze.loc[self.maze['cell']==cell_1,'N']=1
                self.maze.loc[self.maze['cell']==cell_2, 'S']=1
            elif cell_1[1] == cell_2[1] - 1:
                self.maze.loc[self.maze['cell']==cell_1,'S']=1
                self.maze.loc[self.maze['cell']==cell_2,'N']=1
            else:
                raise ValueError('Problem defining the wall, cells incorrect')
        elif cell_1[1] == cell_2[1]:
            if cell_1[0] == cell_2[0] +1 :
                self.maze.loc[self.maze['cell']==cell_1,'E']=1
                self.maze.loc[self.maze['cell']==cell_2,'W']=1
            elif cell_1[0] == cell_2[0] - 1:
                self.maze.loc[self.maze['cell']==cell_1,'W']=1
                self.maze.loc[self.maze['cell']==cell_2,'E']=1
            else:
                raise ValueError('Problem defining the wall, cells incorrect')
        else:
            raise ValueError('Problem defining the wall, cells incorrect')

    def add_outer_walls(self):
        for i in range(self.size[0]):
            self.maze.loc[self.maze['cell']==(i,0),'N']=1
            self.maze.loc[self.maze['cell']==(i,self.size[1]-1),'S']=1
        for i in range(self.size[1]):
            self.maze.loc[self.maze['cell']==(0,i),'E']=1
            self.maze.loc[self.maze['cell']==(self.size[1]-1,i),'W']=1

    def save(self, fname):

        with open(fname, 'wb') as ff:
            pickle.dump(self.__dict__, ff)

    def load(self, fname):
        with open(fname, 'rb') as ff:
            dico = pickle.load(ff)
        self.__dict__.update(dico)
        self.current_pos = list(self.init_pos)



def make_random_maze(size):
    nx, ny = size
    # Maze entry position
    ix, iy = np.random.randint(nx),np.random.randint(ny)
    maze = RMaze(nx, ny, ix, iy)
    maze.make_maze()
    #maze.write_svg('maze.svg')
    new_maze = Maze(size=[maze.nx, maze.ny])
    new_maze.init_pos = maze.init_pos
    new_maze.goal = maze.goal
    for i in range(maze.nx * maze.ny):
        cell = new_maze.maze.iloc[i]['cell']
        walls = maze.cell_at(cell[0], cell[1]).walls
        new_maze.maze.iloc[i,new_maze.maze.columns.get_loc('N')] = int(walls['N'])
        new_maze.maze.iloc[i,new_maze.maze.columns.get_loc('S')] = int(walls['S'])
        new_maze.maze.iloc[i,new_maze.maze.columns.get_loc('W')] = int(walls['E'])
        new_maze.maze.iloc[i,new_maze.maze.columns.get_loc('E')] = int(walls['W'])
    new_maze.add_outer_walls()

    return new_maze
