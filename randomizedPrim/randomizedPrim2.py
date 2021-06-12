#have a dictionary with 1 tuple (x, y) as a key per cell in maze, every key will have a Bool True or False value

# set dict(curent cell) to true
# for the current cell:
#     add random neighbor to stack if dict(neighbor coord) is false
#     set neighbor to current cell and set dict(neighbor coord) to true
#     if no neighbors are false, pop currentcell from stack
#     set popped value to current cell


import random
def gridCreator(row,col):
    
    grid = []

    for i in range(row):
        row = []
        for j in range(col):
            row.append('c')
        grid.append(row)
    
    return(grid)

def printGrid(grid):
    for r in grid:
        print(r)
        print 

def mazeGen(row, col):
    maze = gridCreator(row, col)
    dictionary = {}
    for i in range(0,row):
        for j in range(0,col):
            dictionary[(i,j)] = False
    # print(dictionary)

    startingCell = (0,0)
    maze[startingCell[0]][startingCell[1]] = '.'

    stackOfCells = []

    dictionary[startingCell] = True
    stackOfCells.append(startingCell)
    while stackOfCells:
        neighbors = []
        currentCell = stackOfCells.pop()
        if currentCell[0] == 0: #if first row, only add southern neighbor
            neighbors.append((currentCell[0]+1, currentCell[1]))
        elif currentCell[0] == row-1: #if first row, only add northern neighbor
            neighbors.append((currentCell[0]-1, currentCell[1]))
        else:
            neighbors.append((currentCell[0]+1, currentCell[1]))
            neighbors.append((currentCell[0]-1, currentCell[1]))
        
        if currentCell[1] == 0: #if first col, only add eastern neighbor
            neighbors.append((currentCell[0], currentCell[1]+1))
        elif currentCell[1] == col-1: #if first row, only add western neighbor
            neighbors.append((currentCell[0], currentCell[1]-1))
        else:
            neighbors.append((currentCell[0], currentCell[1]+1))
            neighbors.append((currentCell[0], currentCell[1]-1))
        
        # print(neighbors)
        while (neighbors):
            tempCell = neighbors[random.randrange(0,len(neighbors))]
            # print(tempCell)
            if(dictionary[tempCell]) == False:
                stackOfCells.append(currentCell)
                stackOfCells.append(tempCell)
                dictionary[tempCell] = True
                maze[tempCell[0]][tempCell[1]] = '.'
                printGrid(maze)
                print()

                currentCell = tempCell
                break
            else:
                neighbors.remove(tempCell)
        # print(stackOfCells)

mazeGen(5, 5)