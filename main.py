from maze_baseclass import Maze, make_random_maze
import curses
from curses import wrapper
from curses import panel
import numpy as np
import time
# TODO :
#       one function for each type of maze,
#       Tilt maze with rooms.
#       Tilt maze with multiple goals
#       binaural sound ?
#       Have a ladder to go up the walls ?
#       have a submenu setting.



class Main(object):
    def __init__(self, stdscreen, tilt=False):
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.tilt = tilt
        self.maze = Maze()
        tilt_mazes = [("Tilt maze "+str(f), self.load_maze,{"num":f, "tilt":True, "name":"Tilt Maze "+str(f)}) for f in range(1, 8)]
        self.menu_items = [
            ("How to",  self.how_to,{}),
            ("Beginner Maze 1",  self.load_maze,{"num":1, "tilt":False, "name":"Beginner Maze 1"}),
            ("Beginner Maze 2",  self.load_maze,{"num":1, "tilt":False, "name":"Beginner Maze 2"})]+[
            ("Random Maze",self.generate_random_maze,{}),
        ]+tilt_mazes+[('How to cheat', self.cheat,{})]
        self.menu_items.append(("exit", "exit"))

    def load_maze(self, num, tilt, name):
        if tilt :
            dir = "tilt/"
        else:
            dir = "not_tilt/"
        self.tilt = tilt
        fname = dir+'maze'+str(num)+'.pickle'
        self.maze.load(fname)
        self.display_maze(name)

    def generate_random_maze(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        self.window.refresh()
        curses.doupdate()
        curses.echo()
        self.window.addstr(1,1, "Which size ?")
        self.window.refresh()
        choice = self.window.getstr(2, 1, 20).decode("utf-8")
        curses.noecho()

        if np.char.isnumeric(choice):
            f = int(choice)
            self.maze = make_random_maze((f,f))
            self.display_maze("Random maze of size "+str(f)+'x'+str(f))
        elif choice == "q":
            pass
        else:
            self.window.addstr("\n")
            self.window.addstr(1,1,"Size not understood.")
            self.window.refresh()
            time.sleep(2)
            self.generate_random_maze()

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.menu_items):
            self.position = len(self.menu_items) - 1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.menu_items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = "%d. %s" % (index, item[0])
                self.window.addstr(1 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                if self.position == len(self.menu_items) - 1:
                    break
                else:
                    self.menu_items[self.position][1](**self.menu_items[self.position][2])

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)
            elif key == ord('q'):
                break

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def display_maze(self, name):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        self.window.addstr(1,1,name)
        self.window.addstr(3,1,'Use the arrow keys to move')
        self.window.addstr(4,1,'Press space to describe your immediate surroundings')
        self.window.addstr(5,1,'Press enter to know how far is the exit')
        self.window.addstr(6,1,'Press "q" to quit')


        while True:
            self.window.refresh()
            curses.doupdate()
            key = self.window.getch()

            if key == ord(" "):
                self.maze.describe_cell()

            elif key == curses.KEY_LEFT:
                self.maze.go("left", self.tilt)

            elif key == curses.KEY_RIGHT:
                self.maze.go("right", self.tilt)


            elif key == curses.KEY_DOWN:
                self.maze.go("down", self.tilt)

            elif key == curses.KEY_UP:
                self.maze.go("up", self.tilt)

            elif key in [curses.KEY_ENTER, ord("\n")]:
                self.maze.where_goal()
            elif key == ord("q"):
                break
            else:
                pass

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def cheat(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        self.window.addstr(1,1,"How to cheat.")
        self.window.addstr(3,1,"Cheating is bad, don't do it.")
        self.window.addstr(6,1,"If you still want to cheat, you can look at the image files.")
        self.window.addstr(7,1,"The image files are in the sources in the folders tilt and not_tilt.")
        self.window.addstr(8,1,"One png corresponds to one maze.")


        while True:
            self.window.refresh()
            curses.doupdate()
            key = self.window.getch()
            if key == ord("q"):
                break
            else:
                pass

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    def how_to(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        self.window.addstr(1,1,"How to.")
        self.window.addstr(3,1,"You are in a maze and you have to find the exit.")
        self.window.addstr(4,1,"You can't see but you can sense the walls around you and how far is the exit.")
        self.window.addstr(6,1,"Controls:")
        self.window.addstr(7,3,'Press space to describe your immediate surroundings:')
        self.window.addstr(8,5,'First sound is left, second is up, third is right fourth is down.')
        self.window.addstr(9,5,'You always stay in the same direction, up then right then down is equivalent to right.')
        self.window.addstr(10,5,'High-pitched sound = no wall. Low-pitched = wall.')
        self.window.addstr(11,3,'Use the arrow keys to move')
        self.window.addstr(12,5,'In generic mazes you only move by one step at a time and you get a sound if you try to go through a wall.')
        self.window.addstr(13,5,'In Tilt mazes you always move al the way in the direction you try to go.')
        self.window.addstr(14,5,'As though you were a marble and the maze was tilted in the direction you go.')
        self.window.addstr(15,3,'Press enter to know how far is the exit from current position.')
        self.window.addstr(16,5,'The number of times you ear a sound indicate your distanceto the exit.')
        self.window.addstr(17,5,'The distance used is the Manhattan distance, see wikipedia.')
        self.window.addstr(18,3,'Press "q" to quit')


        while True:
            self.window.refresh()
            curses.doupdate()
            key = self.window.getch()
            if key == ord("q"):
                break
            else:
                pass

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()





class MyApp(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)
        curses.noecho()
        main_menu = Main(self.screen, False)
        main_menu.display()
if __name__ == "__main__":
    curses.wrapper(MyApp)
