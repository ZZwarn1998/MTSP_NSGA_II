import math


class Node:
    # Constructor
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    # Obtain x
    def get_x(self):
        return self.x

    # Obtain y
    def get_y(self):
        return self.y

    # Returns distance to the Node
    def distance_to(self, site):
        xDis = abs(self.get_x() - site.get_x())
        yDis = abs(self.get_y() - site.get_y())
        dis = math.sqrt((xDis * xDis) + (yDis * yDis))
        return dis

    # Gives string representation of the Object with coordinates
    def toString(self):
        s = '(' + str(self.get_x()) + ',' + str(self.get_y()) + ')'
        return s

    # Check if coordinates have been assigned or not
    # Nodes with (-1, -1) as coordinates are created during creation on chromosome objects
    def checkNull(self):
        if self.x == -1:
            return True
        else:
            return False
