import random
import globalManager as gm
from nodeManager import nodeManager
import copy


class Chromosome:
    def __init__(self, gen):
        self.gen = gen

    # def toString(self):
    #     return self.gen

    def getPart1(self):
        part1 = copy.deepcopy(self.gen[: -(gm.get_value("m") - 1)])
        return part1

    def getPart2(self):
        part2 = copy.deepcopy(self.gen[len(self.gen) - (gm.get_value("m") - 1):])
        return part2
