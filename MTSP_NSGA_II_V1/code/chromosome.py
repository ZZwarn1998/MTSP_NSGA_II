import random
import globalManager as gm
from nodeManager import nodeManager
import copy

class chromosome:
    def __init__(self, p1 = None, p2 = None):
        if p1 == None and p2 == None:
            self.part1 = [i for i in range(1, gm.get_value('n'))]
            random.shuffle(self.part1)
            self.part2 = sorted(random.sample(range(1, gm.get_value('n')), gm.get_value('m')-1))
        else:
            self.part1 = copy.copy(p1)
            self.part2 = copy.copy(p2)

        temp = copy.deepcopy(self.part1)
        temp.extend(copy.deepcopy(self.part2))
        self.all = copy.deepcopy(temp)
        self.decode = self.decoding()
        self.distance = None
        self.fitness = None

    def toString(self):
        decodeplus = copy.deepcopy(self.decode)
        decodeplus.append(0)
        route = []
        print("$$",decodeplus)
        for i in range(len(decodeplus)):
            if decodeplus[i] == 0 and i != 0 and i != len(decodeplus) - 1:
                print(route)
                route = [str(decodeplus[i]) + "->" + str(decodeplus[i+1])]
            elif decodeplus[i] == 0 and i == len(decodeplus) - 1:
                print(route)
            else:
                route.append(str(decodeplus[i]) + "->" + str(decodeplus[i+1]))

    def decoding(self):
        decode = []
        splitdots = [0]
        splitdots.extend(copy.deepcopy(self.part2))
        splitdots.append(len(self.part1))

        for index in range(len(splitdots) - 1):
            decode.append(0)
            decode.extend(copy.deepcopy(self.part1[splitdots[index]:splitdots[index + 1]]))

        return decode

    def calFitness(self):
        if self.distance == None:
            self.fitness = 1 / self.calDistance()
        else:
            self.fitness = 1 / self.distance
        return self.fitness

    def calDistance(self):
        dis = 0
        decodeplus = copy.deepcopy(self.decode)
        decodeplus.append(0)
        for index in range(len(decodeplus) - 1):
            fromnode = nodeManager.getNode(decodeplus[index])
            tonode = nodeManager.getNode(decodeplus[index + 1])

            """ COUNT? """

            # distance calculations of pairwise cities
            pdis = fromnode.distance_to(tonode)
            dis = dis + pdis
        self.distance = dis
        return dis

    def getDistance(self):
        if self.distance == None:
            return self.calDistance()
        return self.distance

    def getFitness(self):
        if self.fitness == None:
            return self.calFitness()
        return self.fitness

    def getpart1(self):
        return copy.deepcopy(self.part1)

    def getpart2(self):
        return copy.deepcopy(self.part2)

    def getdecode(self):
        return self.decode



