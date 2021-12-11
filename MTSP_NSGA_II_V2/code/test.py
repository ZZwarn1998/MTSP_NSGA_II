import random
from Node import Node
import globalManager as gm
from nodeManager import nodeManager
from chromosome import Chromosome
from GA import GA
import numpy as np
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

    m = 5
    populationSize = 100
    coeOfDisCal = 20000
    generation = 200
    seedValue = 1
    tournamentSize = 2
    mutationRate = 0.1

    filename = ["mtsp51", "mtsp100", "mtsp150", "pr76", "pr152", "pr226"]
    # filename = ["mtsp51", "mtsp100"]
    solution_summary = {}
    solution_detail = {}
    for data_name in filename:
        path_solution = []
        optimal_solution = []
        run_time = []
        for round in range(30):
            init(data_name, m, populationSize, coeOfDisCal, generation, seedValue, tournamentSize, mutationRate)
            pop = [Chromosome(randomly_generate()) for i in range(0, gm.get_value("popSize"))]
            runtime, best, f1valbest, f2valbest, number, minfun1val_per_round, minfun2val_per_round = GA.start(pop)
            dis_list = []
            for i in range(len(best)):
                dis_list.append(f1valbest[i])

            optimal_solution.append(int(min(dis_list)))
            run_time.append(int(runtime))
            path_solution.append(best[dis_list.index(min(dis_list))].getPart1())

        one_solution = {"solution": optimal_solution,
                        "runtime": run_time,
                        "best_solution": min(optimal_solution),
                        "worst_solution": max(optimal_solution),
                        "average_solution:": np.array(optimal_solution).mean(),
                        "average_time": np.array(run_time).mean()}

        detail_solution = {"all_solution": path_solution,
                           "best_solution": min(optimal_solution),
                           "best_solution_path": path_solution[optimal_solution.index(min(optimal_solution))]}

        solution_summary.update({data_name: one_solution})
        solution_detail.update({data_name: detail_solution})
    print(solution_summary)
    print(solution_detail)
    np.save('summary.npy', solution_summary)
    np.save('summary_detail.npy', solution_detail)
