import random
from Node import Node
import globalManager as gm
from nodeManager import nodeManager
from chromosome import Chromosome
from GA import GA
import matplotlib.pyplot as plt


def randomly_generate():
    part1 = random.sample(range(1, gm.get_value("n")), gm.get_value("n") - 1)
    part2 = [i + num for i, num in
             enumerate(sorted(random.sample(range(2, gm.get_value("n") - 3), gm.get_value("m") - 1)))]
    return part1 + part2


def init(filename, m, populationSize, coeOfDisCal, generation, seedValue, tournamentSize, mutationRate):
    # Initialization of globalManager
    gm._init()

    # Load data
    path = "..//data//" + filename + ".txt"
    file = open(path, 'r')
    n = -1
    for index, row in enumerate(file):
        if index == 0:
            row = row.strip()
            n = int(row)
        else:
            row = row.strip()
            elems = row.split(' ')
            node = Node(int(elems[1]), int(elems[2]))
            nodeManager.addNode(node)

    # the Number of nodes
    gm.set_value("n", n)
    # the Number of travel salesmen
    gm.set_value("m", m)
    # the Size of population
    gm.set_value("popSize", populationSize)
    # Number of distance calculations of pairwise cities
    gm.set_value("coe", coeOfDisCal * gm.get_value("n"))
    # Number of Generation
    gm.set_value("gene", generation)
    # SeedValue
    gm.set_value("seedValue", seedValue)
    # Tournament size
    gm.set_value("tSize", tournamentSize)
    # Mutation Rate
    gm.set_value("mr", mutationRate)


if __name__ == "__main__":
    filename = "pr226"
    m = 5
    populationSize = 100
    coeOfDisCal = 20000
    generation = 200
    seedValue = 1
    tournamentSize = 2
    mutationRate = 1

    # import data and initialize global parameters
    init(filename, m, populationSize, coeOfDisCal, generation, seedValue, tournamentSize, mutationRate)

    pop = [Chromosome(randomly_generate()) for i in range(0, gm.get_value("popSize"))]
    runtime, best, f1valbest, f2valbest, number, minfun1val_per_round, minfun2val_per_round = GA.start(pop)
    print(f"Runtime: {runtime}")

    print(f"The best path(s) for Generation number {generation} is:")
    print("Number of solutions:", number)
    for i in range(len(best)):
        print("No.", i + 1)
        print("part1:", best[i].getPart1())
        print("part2:", best[i].getPart2())
        print("Function1:", f1valbest[i])
        print("Function2:", f2valbest[i])

    plt.figure(1)
    plt.plot(range(0, generation), minfun1val_per_round)
    plt.title("FUN1")
    plt.figure(2)
    plt.title("FUN2")
    plt.plot(range(0, generation), minfun2val_per_round)
    plt.show()
