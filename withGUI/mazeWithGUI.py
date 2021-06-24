#created using inspiration from Wikipedia for algorithms and Ali Mahmoud for GUI

from tkinter import *
from random import randrange
import time
import colorFile

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
lastCell = 0
stackOfCells = []
solvingStack = []
visitedStack = [] 

#initialize the maze gui and the canvassing
gui = Tk()
gui.title("Randomized Maze Generator")
layout = Canvas(gui,width=x, height=y, bg='white')
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

        #use create_line function to to draw lines for each cell
        #coordinates reflect start and end of a line
        self.topLine = layout.create_line(x, y, x+divider, y, fill="black", width = 3)
        self.rightLine = layout.create_line(x+divider, y, x+divider, y+divider, fill="black", width = 3)
        self.bottomLine = layout.create_line(x, y+divider, x+divider, y+divider, fill="black", width = 3)
        self.leftLine = layout.create_line(x, y, x, y+divider, fill="black", width = 3)

    def displayVisited(self):
        #initializing coordinates of the cell
        x = self.xCoord*divider
        y = self.yCoord*divider

        #for visited cells we create a small rectangle as we visit a given cell
        if self.visited == True:
            self.rectangle = layout.create_rectangle(x+3, y+3, x+divider-3, y+divider-3, fill='white', outline='')
            gui.update()

    def highlight(self):
        #initializing coordinates of the cell
        x = self.xCoord*divider
        y = self.yCoord*divider
        
        #since it is a moving and temporary cell (currentCell) no need to set a variable
        layout.create_rectangle(x+3, y+3, x+divider-3, y+divider-3, fill='red', outline='')
        gui.update()

    def highlightBacktrack(self):
        #initializing coordinates of the cell
        x = self.xCoord*divider
        y = self.yCoord*divider
        
        #since it is a moving and temporary cell (currentCell) no need to set a variable
        color = colorFile.COLORS[randrange(len(colorFile.COLORS))]
        layout.create_rectangle(x+1, y+1, x+divider-1, y+divider-1, fill='pale green', outline='')
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



def draw():
    #reference the global currentCell to be able to display from inside function
    global currentCell

    for i in range(rows): #row times
        for j in range(cols): #cols time
            maze[i][j].display() #display the referenced cell

    #continuous loop until stack is empty, then break
    while True:
        #for the current cell 1st establish the moving blinker, and secondly mark as visited (can use diff color later)
        currentCell.highlight()
        currentCell.displayVisited()

        #set the nextCell to to be a randomly chosen neighbor of the current cell,
        #there may not be any neighbors which havent been visited
        nextCell = currentCell.checkNeighbors()

        if nextCell: #if a nextCell exists
            #in the display, remove the walls between the current and next cell
            remove_walls(currentCell, nextCell) 

            #add the current cell to the stack of all cells and then the stack to help solve later on
            stackOfCells.append(currentCell)
            solvingStack.append(currentCell)

            #set nextCell to the current cell and mark it now as visited
            currentCell = nextCell
            currentCell.visited = True
            
        #if no neighbors for the given cell, then as long as the list of cells has more cells, then pop one off
        #set that cell to be visited
        elif len(stackOfCells) > 0:
            currentCell = stackOfCells.pop()
            visitedStack.append(currentCell)
        #if no cells in the stack then break out of loop
        else:
            break


def remove_walls(curr, next):
    #initialize vertical as the difference between next and current xCoord
    #initialize horizontal as the difference between next and currenct yCoord
    vertical = curr.xCoord - next.xCoord
    horizontal = curr.yCoord - next.yCoord

    #if we are on the same row
    if horizontal == 0:
        if vertical == -1: #if we are moving right, remove the right wall of current and left wall of next
            layout.delete(curr.rightLine)
            layout.delete(next.leftLine)
            curr.walls[1] = False
            next.walls[3] = False
            gui.update()

        elif vertical == 1: #if we are moving left, remove the left wall of current and right wall of next
            layout.delete(curr.leftLine)
            layout.delete(next.rightLine)
            curr.walls[3] = False
            next.walls[1] = False
            gui.update()
    
    #if we are on the same column
    if vertical == 0:
        if horizontal == -1: #if we are moving down, remove the bottom wall of current and top wall of next
            layout.delete(curr.bottomLine)
            layout.delete(next.topLine)
            curr.walls[2] = False
            next.walls[0] = False
            gui.update()

        elif horizontal == 1: #if we are moving up, remove the top wall of current and bottom wall of next
            layout.delete(curr.topLine)
            layout.delete(next.bottomLine)
            curr.walls[0] = False
            next.walls[2] = False
            gui.update()

#=================

def solve():
    global currentCell
   
    currentCell = maze[0][0]
    secondCell = maze[0][1]
    stackOfCells = []

    dictionary = {}
    for i in range(rows):
        for j in range(cols):
            dictionary[(i,j)] = False

    xCoord = currentCell.xCoord
    yCoord = currentCell.yCoord
    
    dictionary[(xCoord,yCoord)] == True
    stackOfCells.append(currentCell)

    # secondCell.highlight()
    # gui.update()

    # return
    while stackOfCells:
        neighbors = []
        currentCell = stackOfCells.pop()
        if currentCell.yCoord == rows-1 and currentCell.xCoord == cols-1:
            #currentCell.highlight()
            stackOfCells.append(currentCell)
            break
        if currentCell.yCoord == 0: # if top row, then cannot have north
            if currentCell.xCoord != 0: #if not top left corner, can check west
                if currentCell.walls[3] == False:
                    neighbors.append(maze[currentCell.xCoord-1][currentCell.yCoord])
            if currentCell.xCoord != cols-1: #if not top right corner, can check east
                if currentCell.walls[1] == False:
                    neighbors.append(maze[currentCell.xCoord+1][currentCell.yCoord])
            
            if currentCell.walls[2] == False: #all top row can check south
                neighbors.append(maze[currentCell.xCoord][currentCell.yCoord+1])    

        elif currentCell.yCoord == rows-1: # if bottom row, then cannot have south
            if currentCell.xCoord != 0: #if not bottom left corner, can check west
                if currentCell.walls[3] == False:
                    neighbors.append(maze[currentCell.xCoord-1][currentCell.yCoord])
            if currentCell.xCoord != cols-1: #if not bottom right corner, can check east
                if currentCell.walls[1] == False:
                    neighbors.append(maze[currentCell.xCoord+1][currentCell.yCoord])
            
            
            if currentCell.walls[0] == False: #all bottom row can check north
                neighbors.append(maze[currentCell.xCoord][currentCell.yCoord-1]) 
        
        elif currentCell.yCoord > 0 and currentCell.yCoord < rows-1: #all rows in between can check north and south
            
            if currentCell.walls[0] == False: #all rows can check north
                neighbors.append(maze[currentCell.xCoord][currentCell.yCoord-1]) 
            if currentCell.walls[2] == False: #all rows can check south
                    neighbors.append(maze[currentCell.xCoord][currentCell.yCoord+1]) 
            
            if currentCell.xCoord != 0: #if not left edge, can check west
                if currentCell.walls[3] == False:
                    neighbors.append(maze[currentCell.xCoord-1][currentCell.yCoord])
            if currentCell.yCoord != cols-1: #if not right edge, can check east
                if currentCell.walls[1] == False:
                    neighbors.append(maze[currentCell.xCoord+1][currentCell.yCoord])
        
        # for elements in neighbors:
        #     print((elements.xCoord,elements.yCoord))
        
       
        while neighbors:
            randomCell = neighbors[randrange(len(neighbors))]
            for elements in neighbors:
                print((elements.xCoord,elements.yCoord))
            print("Coords are: " + str((randomCell.xCoord,randomCell.yCoord)))
            print ("Visited?: " + str(dictionary[(randomCell.xCoord,randomCell.yCoord)]))

            
            if dictionary[(randomCell.xCoord,randomCell.yCoord)] == False:
                stackOfCells.append(currentCell)
                stackOfCells.append(randomCell)
                dictionary[(randomCell.xCoord,randomCell.yCoord)] = True
                # currentCell.highlight()
                # gui.update()
                # time.sleep(.1)
                currentCell = randomCell #not so useful because we set it again at the top of the loop
                break
            else:
                neighbors.remove(randomCell)
                # randomCell.highlight()
    
    for cell in stackOfCells:
        cell.highlightBacktrack()
        gui.update()
        time.sleep(.05)
        # print((cell.xCoord,cell.yCoord))


            

            

    #at this point there exists a maze
    #every cell has top, bottom, left and right lines as True or False in a list
    #a neighbor is a cell in the vicinity without a wall in between aka (neighbor S and current N are both false) and not visited
    
    #for the current cell:
    #   set dict(current cell) to true (done)
    #   add current cell to stackofcells (done)
    #   while the stackofcells is not empty:
        #   find  valid neighbors of stackofcells.pop(), add them to neighbor list (no wall)
        #   for all the neighbors:
            #   if the dict(neighbor cell) == False
            #       append current cell to stackofcells
            #       append neighbor cell to stackofcells
            #       highlight the neighbor cell and update GUI
            #       set dictionary(neighbor cell) to True
            #       set current cell to neighbor cell
            #       break
            #   else
            #       remove the neighbor from the list
    

        
    

        
        





    

if __name__ == '__main__':
    setup()
    draw()
    start = layout.itemconfigure(maze[0][0].rectangle, fill='red')
    end = layout.itemconfigure(maze[rows-1][cols-1].rectangle, fill='green')
    Label(gui, text='Made by: Siddhartha Bose', fg='red', bg='white').pack(side=RIGHT)

    layout.update()
    gui.update()
    
    button = Button(gui, text='Show Correct Path', command=solve).pack()

    gui.mainloop()