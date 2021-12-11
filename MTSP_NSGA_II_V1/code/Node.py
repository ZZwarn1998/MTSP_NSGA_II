import math
class Node:
    # Constructor
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    # Obtain x
    def getX(self):
        return self.x

    # Obtain y
    def getY(self):
        return self.y

    # Returns distance to the Node
    def distanceTo(self, site):
        xDis = abs(self.getX() - site.getX())
        yDis = abs(self.getY() - site.getY())
        dis = math.sqrt((xDis * xDis) + (yDis * yDis))
        return dis

    # Gives string representation of the Object with coordinates
    def toString(self):
        s = '(' + str(self.getX()) + ',' + str(self.getY()) + ')'
        return s

    # Check if coordinates have been assigned or not
    # Nodes with (-1, -1) as coordinates are created during creation on chromosome objects
    def checkNull(self):
        if self.x == -1:
            return True
        else:
            return False
