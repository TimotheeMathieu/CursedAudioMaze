from tkinter import Tk, Canvas, Frame, BOTH
from maze_baseclass import Maze
import tkcap
import os


class Maze_creator(Frame):

    def __init__(self,root,  size=(6,6), pixel = 200,fname ="maze.picvle"):
        super().__init__()
        self.size = size
        self.pixel = pixel
        self.maze = Maze(size=size)
        self.maze.add_outer_walls()
        self.first_cell = True
        self.cell_1 = None
        cap = tkcap.CAP(root)
        if not os.path.isfile(fname.split('.')[0]+'.png'):
            cap.capture(fname.split('.')[0]+'.png')

        def click(event):
            x, y = event.x, event.y
            cell = (x//pixel,y//pixel)
            if self.first_cell:
                self.first_cell = False
                self.cell_1 = cell
            else:
                self.first_cell = True
                self.maze._add_wall(self.cell_1, cell)
                self.draw_wall(self.cell_1, cell)
                self.maze.save(fname)
                cap.capture(fname.split('.')[0]+'.png',overwrite=True)
        def set_goal(event):
            x, y = event.x, event.y
            cell = (x//pixel,y//pixel)
            self.maze.goal = cell
            self.maze.save(fname)
            cap.capture(fname.split('.')[0]+'.png',overwrite=True)
            self.canvas.create_oval(x//pixel*pixel, y//pixel*pixel,
                                    (x//pixel+1)*pixel , (y//pixel+1)*pixel
                                    ,fill="red")

        def set_init(event):
            x, y = event.x, event.y
            cell = (x//pixel,y//pixel)
            self.maze.init_pos = cell
            self.maze.save(fname)
            cap.capture(fname.split('.')[0]+'.png',overwrite=True)
            self.canvas.create_oval(x//pixel*pixel, y//pixel*pixel,
                                    (x//pixel+1)*pixel , (y//pixel+1)*pixel
                                    ,fill="green")

        root.bind("<Button-1>", click)
        root.bind('<Button-2>', set_goal)
        root.bind('<Button-3>', set_init)
        root.bind('q', "exit")


        self.initUI()

    def initUI(self):

        self.master.title("Maze")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.create_rectangle(0, 0, self.size[0]*self.pixel, self.size[1]*self.pixel, outline="black", fill="white")
        for i in range(self.size[0]):
            self.canvas.create_line(0, i*self.pixel, self.size[1]*self.pixel, i*self.pixel,width=self.pixel/60)
        for j in range(self.size[1]):
            self.canvas.create_line( j*self.pixel, 0, j*self.pixel, self.size[0]*self.pixel,width=self.pixel/60)


        self.canvas.pack(fill=BOTH, expand=1)

    def draw_wall(self, cell_1, cell_2):

        if cell_1[0] == cell_2[0]:
            x1 =  cell_1[0]*self.pixel
            x2 = (cell_1[0]+1)*self.pixel
            if cell_1[1] == cell_2[1] +1 :
                y1 = y2 = cell_1[1]*self.pixel
            elif cell_1[1] == cell_2[1] - 1:
                y1 = y2 = (cell_1[1]+1)*self.pixel
            else:
                pass
        elif cell_1[1] == cell_2[1]:
            y1 = cell_1[1]*self.pixel
            y2 = (cell_1[1]+1)*self.pixel
            if cell_1[0] == cell_2[0] +1 :
                x1 = x2 = self.pixel*cell_1[0]
            elif cell_1[0] == cell_2[0] - 1:
                x1 = x2 = self.pixel*(cell_1[0]+1)
            else:
                pass
        else:
            pass
        print(x1, x2, y1, y2)
        self.canvas.create_line(x1,y1, x2, y2,width=self.pixel/30)


def main():
    size = (9,9)
    pixel = 200
    fname = "tilt/maze7.pickle"
    size_window=(str(size[0]*pixel), str(size[1]*pixel))
    root = Tk()

    Maze_creator(root, size, pixel, fname = fname)
    root.geometry(size_window[0]+'x'+size_window[1]+"+0+0")
    root.mainloop()



if __name__ == '__main__':
    main()
