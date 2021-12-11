'''
just for testing
'''


import globalManager as gm
from nodeManager import *
from chromosome import chromosome
from Population import Population
def init():
    print(gm.get_value("n"),\
    gm.get_value("m"),\
    gm.get_value("cons"),\
    gm.get_value("size"),\
    gm.get_value("runs"))
    for i in range(0,gm.get_value('n')):
        print(nodeManager.getNode(i).toString())
    c = chromosome()
    c.toString()
    print(c.decoding())
    print(c.calDistance())
    pop = Population(gm.get_value('size'))
    pop.getBestChromosome().toString()



if __name__ == "__main__":
    init()