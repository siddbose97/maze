#logic inspired by Christian Hill 2017

#create a cell class to instantiate cells within the grid which will house the maze
#every cell will have walls and a coordinate pair

class cell:
    # create pairs of walls
    wallPairs = {"N":"S", "S":"N", "E":"W", "W":"E"}

    def __init__(self, x, y):
        #give a wall coordinates xy and then give it walls (all bool true)
        self.xCoord = x
        self.yCoord = y
        self.walls = {"N": True, "S": True, "E": True, "W": True}
        
    def checkWalls(self):
        #check if all walls are still present
        for key in self.walls:
            if self.walls[key] == True:
                continue
            else:
                return False
        return True

    def removeWall(self, neighbor, wall):
        #if removing one wall for a cell, remove corresponding wall in other cell
        if self.walls[wall] == False:
            neighborWall = cell.wallPairs[wall]
            neighbor.walls[neighborWall] = False #use corresponding wall to remove accordingly
        
            
class maze:
    #initialize a maze as cells in rows and columns based on input values
    #initialize by taking input row and column and then using 0,0 as a starting cell

    

    pass

