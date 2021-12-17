from galogic import *
import progressbar
import time
import nodenum as nn
import json

pbar = progressbar.ProgressBar()


def load_from_file(filepath):
    RouteManager.clear()
    node_list = []
    f = open(filepath)  # 返回一个文件对象
    for line in f.readlines():
        line = line.strip('\n').split(' ')
        if len(line) == 1:
            None
            nn._init(int(line[0]))
        else:
            x = int(line[1])
            y = int(line[2])
            node_list.append((x, y))
    for i in node_list:
        RouteManager.addDustbin(Dustbin(i[0], i[1]))


# fig = plt.figure()
#
# plt.plot(xaxis, yaxis, 'r-')
# plt.show()


def start(problem_path):
    load_from_file(problem_path)
    yaxis = []  # Fittest value (distance)
    pop = Population(populationSize, True)
    globalRoute = pop.getFittest()
    print('Initial minimum distance: ' + str(globalRoute.getDistance()))

    start_time = time.time()
    # Start evolving
    for i in range(numGenerations):
        pop = GA.evolvePopulation(pop)
        localRoute = pop.getFittest()
        if globalRoute.getDistance() > localRoute.getDistance():
            globalRoute = localRoute
        yaxis.append(localRoute.getDistance())
    end_time = time.time()
    runtime = end_time - start_time
    optimal_length = globalRoute.getDistance()
    optimal_path = globalRoute.to_list()
    optimal_per_round = yaxis

    return runtime, optimal_length, optimal_path, optimal_per_round


if __name__ == "__main__":

    record_dict = {}

    #for data_name in ["mtsp51", "mtsp100", "mtsp150", "pr76", "pr152", "pr226"]:
    for data_name in ["mtsp51", "mtsp100"]:
        tmp_dict = {}
        run_time_all = []
        optimal_length_all = []
        optimal_path_all = []
        minfun1val_per_round_all = []

        for i in range(2):
            print(i)
            path = "./data/" + data_name + ".txt"
            runtime, optimal_length, optimal_path, minfun1val_per_round = start(path)
            run_time_all.append(runtime)
            optimal_length_all.append(optimal_length)
            optimal_path_all.append(optimal_path)
            minfun1val_per_round_all.append(minfun1val_per_round)
        tmp_dict = {"run_time": run_time_all,
                    "optimal_length": optimal_length_all,
                    "optimal_path": optimal_path_all,
                    "minfun2val_per_round": minfun1val_per_round_all}
        record_dict.update({data_name: tmp_dict})
    print(record_dict)

    data = json.dumps(record_dict, indent=1)
    with open("./record_base.json", "w") as f:
        f.write(data)


