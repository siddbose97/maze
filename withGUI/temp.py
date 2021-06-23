







def draw_solve():
    global currentCell
    solvingStack.reverse()
    visitedStack.reverse()
    currentCell = solvingStack.pop()



    while True:
        xCoord= currentCell.xCoord
        yCoord = currentCell.yCoord
        if xCoord== rows-1 and yCoord == cols-1:
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
            if len(visitedStack) > 0:
                currentCell = visitedStack.pop()
                print("im here")
            gui.update()
            time.sleep(0.1)

def 1 :
    if xCoord == rows-1 and yCoord == cols-1:
        currentCell.highlight()
        return

    stackOfCells.append(currentCell)
    dictionary[(currentCell.xCoord,currentCell.yCoord)] = True
    
    while stackOfCells:
        neighbors = []
        currentCell = stackOfCells.pop()
        
        #set tempCell to a random unvisited neighbor
        tempCell = currentCell.checkNeighbors()

        #if all neighbors have been visited, then pop a cell off the stack and go back
        while tempCell == False and len(stackOfCells) > 0:
            currentCell = stackOfCells.pop()
            tempCell = currentCell.checkNeighbors
            stackOfCells.append(currentCell)

        if(dictionary[(tempCell.xCoord, tempCell.yCoord)]) == False:
            stackOfCells.append(currentCell)
            stackOfCells.append(tempCell)
            dictionary[(tempCell.xCoord, tempCell.yCoord)] = True
            currentCell.highlight()
            currentCell = tempCell
            gui.update()
            time.sleep(0.1)
            break
        else:
            neighbors.remove(tempCell)