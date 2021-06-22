#created using inspiration from Wikipedia for algorithms and Ali Mahmoud for GUI

from tkinter import *
from random import randrange
import time

#
x = 400
y = 400
divider = 40
rows = y//divider
cols = x//divider

maze = [] #create a 2d array using nested loop, research list comprehension later
for i in range(rows):
    row = []
    for j in range(cols):
        row.append([])
    maze.append(row)

#initializing stacks required to traverse through the maze
currentCell = 0
stackOfCells = []
solvingStack = []
visitedStack = [] 

#initialize the maze gui and the canvassing
gui = Tk()
gui.title("Randomized Maze Generator")
layout = Canvas(gui,width=x, height=y, bg='pink')
layout.pack()




class Cell:

    def __init__(self, xCoord, yCoord):
        self.xCoord = xCoord
        self.yCoord = yCoord
        
        #initialize walls around the cell as True for NESW
        self.walls = [True, True, True, True] 
        self.visited = False
        
        #initialize lines around self to be 0
        self.topLine = 0
        self.rightLine = 0
        self.bottomLine = 0
        self.leftLine = 0

        self.chosen = False
        self.rectangle = 0

    def display(self):
        #initializing coordinates of the cell
        x = self.xCoord*divider
        y = self.yCoord*divider

        #use create_line functionto to draw lines for each cell
        #coordinates reflect start and end of a line
        self.topLine = layout.create_line(x, y, x+divider, y, fill="black", width = 2)
        self.rightLine = layout.create_line(x+divider, y, x+divider, y+divider, fill="black", width = 2)
        self.bottomLine = layout.create_line(x, y+divider, x+divider, y+divider, fill="black", width = 2)
        self.leftLine = layout.create_line(x, y, x, y+divider, fill="black", width = 2)
        

    def displayVisited(self):
        #initializing coordinates of the cell
        x = self.xCoord*divider
        y = self.yCoord*divider

        #for visited cells we create a small rectangle as we visit a given cell
        if self.visited == True:
            self.rectangle = layout.create_rectangle(x+3, y+3, x+divider-3, y+divider-3, fill='pink', outline='')
            gui.update()

    def highlight(self):
        #initializing coordinates of the cell
        x = self.xCoord*divider
        y = self.yCoord*divider
        
        #since it is a moving and temporary cell (currentCell) no need to set a variable
        layout.create_rectangle(x+5, y+5, x+divider-5, y+divider-5, fill='red', outline='')
        gui.update()


    def checkNeighbors(self, s=False):
        listOfNeighbors = []

        #check if north is out of bounds
        if checkEdge(self.xCoord-1, self.yCoord) == False:
            north = maze[self.xCoord-1][self.yCoord]
            if north.visited == False:
                listOfNeighbors.append(north)

        #check if east is out of bounds
        if checkEdge(self.xCoord, self.yCoord+1) == False:
            east = maze[self.xCoord][self.yCoord+1]
            if east.visited == False:
                listOfNeighbors.append(east)
        
        #check if south is out of bounds
        if checkEdge(self.xCoord+1, self.yCoord) == False:
            south = maze[self.xCoord+1][self.yCoord]
            if south.visited == False:
                listOfNeighbors.append(south)
        
        #check if west is out of bounds
        if checkEdge(self.xCoord, self.yCoord-1) == False:
            west = maze[self.xCoord][self.yCoord-1]
            if west.visited == False:
                listOfNeighbors.append(west)

        #assuming list of neighbors isnt empty we go to the next neighbor randomly, if empty return false
        if len(listOfNeighbors) > 0:
            nextNeighbor = randrange(len(listOfNeighbors))
            return listOfNeighbors[nextNeighbor]
        else:
            return False


def checkEdge(i, j):
    #if within the maze then return False (not edge) else True
    if i >= 0 and j >= 0 and i < rows and j < cols:
        return False
    else:
        return True
    


def setup():
    #was facing an error when not using global keyword since otherwise we cannot modify within the function
    global currentCell

    for i in range(rows):
        for j in range(cols):
            maze[i][j] = Cell(i, j)

    #setting starting cell as top left and then mark it as visited
    currentCell = maze[0][0] 
    currentCell.visited = True

#=================


def draw():
    global currentCell

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            maze[i][j].display()

    while True:
        currentCell.highlight()
        currentCell.displayVisited()

        # STEP 1
        next_cell = currentCell.checkNeighbors()
        if next_cell:

            # STEP 2
            stackOfCells.append(currentCell)
            solvingStack.append(currentCell)

            # STEP 3
            remove_walls(currentCell, next_cell) #######

            # STEP 4
            currentCell = next_cell
            currentCell.visited = True

        elif len(stackOfCells) > 0:
            currentCell = stackOfCells.pop()
            visitedStack.append(currentCell)
        else:
            break


def remove_walls(c, n):
    y = c.xCoord- n.xCoord
    x = c.yCoord - n.yCoord
    if x == 0:
        if y == -1:
            layout.delete(c.rightLine)
            layout.delete(n.leftLine)
            c.walls[1] = False
            n.walls[3] = False
            gui.update()
        elif y == 1:
            layout.delete(c.leftLine)
            layout.delete(n.rightLine)
            c.walls[3] = False
            n.walls[1] = False
            gui.update()

    if y == 0:
        if x == -1:
            layout.delete(c.bottomLine)
            layout.delete(n.topLine)
            c.walls[2] = False
            n.walls[0] = False
            gui.update()
        elif x == 1:
            layout.delete(c.topLine)
            layout.delete(n.bottomLine)
            c.walls[0] = False
            n.walls[2] = False
            gui.update()
            #print(c.__dict__)

def draw_solve():
    global currentCell
    solvingStack.reverse()
    visitedStack.reverse()
    currentCell = solvingStack.pop()

    while True:
        xCoord= currentCell.xCoord
        j = currentCell.yCoord
        if xCoord== rows-1 and j == cols-1:
            currentCell.highlight()
            break

        if not currentCell.chosen:
            currentCell.highlight()
            currentCell.chosen = True
            currentCell = solvingStack.pop()
            gui.update()
            time.sleep(0.1)

        elif currentCell.chosen:
            currentCell.displayVisited()
            currentCell = visitedStack.pop()
            gui.update()
            time.sleep(0.1)

if __name__ == '__main__':
    setup()
    draw()
    button = Button(gui, text='Show Solve!', command=draw_solve).pack()

    def change(event):
        print('Yes!!')
        a = layout.itemconfigure(currentCell.rectangle, fill='green')

        layout.update()
        gui.update()
        b = layout.itemcget(currentCell.rectangle, "fill")
        print('B', b)
    d = layout.bind('<Button-1>', change)
    print('I am bind d = ', d)
    Label(gui, text='Made by: Siddhartha Bose', fg='red', bg='white').pack(side=RIGHT)
    print(len(solvingStack))
    print(solvingStack)
    print(len(visitedStack))

    gui.mainloop()