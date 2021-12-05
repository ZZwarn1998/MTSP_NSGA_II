import copy
from chromosome import chromosome
import globalManager as gm

class Population:
    nodes = []
    def __init__(self, size):
        for i in range(size):
            self.sizeOfPop = size
            chromo = chromosome()
            self.nodes.append(chromo)


    def getBestChromosome(self):
        bestchromo = self.nodes[0]
        for i in range(gm.get_value('size')):
            if bestchromo.getFitness() <= self.nodes[i].getFitness():
                bestchromo = copy.deepcopy(self.nodes[i])
        return bestchromo

    def getChromosome(self, index):
        return self.nodes[index]

    def saveChromosome(self, index, chromo):
        self.nodes[index] = chromo






