from Node import Node
import globalManager as gm
import test as t
import test2 as t2
from nodeManager import nodeManager
from Population import Population
import random
from GA import GA
import matplotlib.pyplot as plt

def init(filename):
    # Initialization of globalManager
    gm._init()

    # Load data
    path = "..//data//" + filename + ".txt"
    file = open(path, 'r')
    N = -1
    for index,row in enumerate(file):
        if index == 0:
            row = row.strip()
            N = int(row)
        else:
            row = row.strip()
            elems = row.split(' ')
            node = Node(int(elems[1]), int(elems[2]))
            nodeManager.addNode(node)

    # the Number of nodes
    gm.set_value("n", N)
    # the Number of travel salesmen
    gm.set_value("m", 5)
    # the Size of population
    gm.set_value("size", 100)
    # Number of distance calculations of pairwise cities
    gm.set_value("cons", 20000*N)
    # Independent runs
    gm.set_value("runs", 200)
    # SeedValue
    gm.set_value("seedvalue", 1)
    # Tournament size
    gm.set_value("tournamentsize", 2)
    # Mutation Rate
    gm.set_value("MR", 0.1)

    # test the usefulness of globalManager
    # t.init()



if __name__ == "__main__":
    filename = "mtsp51"
    init(filename)
    pop = Population(gm.get_value('size'))

    random.seed(gm.get_value("seedvalue"))

    bestAns = pop.getBestChromosome()
    print("Current Optimal Distance:", bestAns.getDistance())

    Y = []
    X = []
    i = 0

    while( i < gm.get_value('runs')):
        pop = GA.evolvePopulation(pop)
        best = pop.getBestChromosome()

        print("ROUND",i,best.getFitness())
        if best.getDistance() < bestAns.getDistance():
            bestAns = best
        Y.append(bestAns.getDistance())
        X.append(i)
        i = i + 1

    print('Global minimum distance: ' + str(bestAns.getDistance()))
    print('Final Route: ')
    bestAns.toString()

    fig = plt.figure()

    plt.plot(X, Y, 'r-')
    plt.show()

