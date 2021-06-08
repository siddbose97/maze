import random
from array import *


#create a grid of however many rows and columns. initialize as only walls
def gridCreator(row,col):
    
    grid = []

    for i in range(row):
        row = []
        for j in range(col):
            row.append('w')
        grid.append(row)
    
    return(grid)

def printGrid(grid):
    for r in grid:
        print(r)
        print 

#check if cell is on the border on the map, therefore which walls to add to the list
def checkBorder(x,y,row,col):
    validCoord = {"N":True,"S":True, "E":True, "W":True}

    if x == 0:
        validCoord["N"] = False
    if x == (row-1):
        validCoord["S"] = False
    if y == 0:
        validCoord["W"] = False
    if y == (col-1):
        validCoord["E"] = False
    
    return(validCoord)

#returns the coordinate of the wall and the direction vis a vis the cell in question
def retWallCoord(coord,wallValue):
    returnValue = (0,0,"")

    if wallValue == "N":
        returnValue = (coord[0]-1, coord[1],wallValue)
    elif wallValue == "S":
        returnValue = (coord[0]+1, coord[1],wallValue)
    elif wallValue == "E":
        returnValue = (coord[0], coord[1]+1,wallValue)
    elif wallValue == "W":
        returnValue = (coord[0], coord[1]-1,wallValue)
    
    return returnValue

def checkNumVisited(coord, row, col, maze):
    numVisited = 0
    x = coord[0]
    y = coord[1]
    typeOfCell = ["N", "S", "E", "W"]

    cellsAroundWall = checkBorder(x, y, row, col)

    for elements in typeOfCell:
        if cellsAroundWall[elements] == True:
            if x != row-1 and elements == "N" and maze[x+1][y] == "c":
                numVisited +=1 
                # print("N")
            if x != 0 and elements == "S" and maze[x-1][y] == "c":
                numVisited +=1 
                # print("S")
            if y != 0 and elements == "E" and maze[x][y-1] == "c":
                numVisited +=1 
                # print("E")
            if y != col-1 and elements == "W" and maze[x][y+1] == "c":
                numVisited +=1 
                # print("W")
    
    return numVisited

def mazeCreator(row,col):
    typeOfWall = ["N", "S", "E", "W"]

    maze = gridCreator(row,col)
    # startingRow = random.randrange(row)-1
    # startingCol = random.randrange(col)-1
    startingRow = 2
    startingCol = 1

    maze[startingRow][startingCol] = 'c'
    listOfWalls = []
    startingCellCoord = (startingRow,startingCol)
    startingCellWalls = checkBorder(startingRow,startingCol,row,col)
    print(startingCellWalls)
    for elements in typeOfWall:
        if startingCellWalls[elements] == True:
            listOfWalls.append(retWallCoord(startingCellCoord,elements))
    

    while len(listOfWalls)>0:
        wallInQuestion = listOfWalls.pop()
        #wallInQuestion = (0,1,"N")
        if checkNumVisited(wallInQuestion, row, col, maze) <=2:
            maze[wallInQuestion[0]][wallInQuestion[1]]= 'c'

    

    


    # print(startingCellWalls)
    printGrid(maze)



mazeCreator(5,5)