from galogic import *
import time
import nodenum as nn
import json
import os.path as osp
import argparse


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


def run_and_save(root_path, problem_name, save_name):
    problem_path = osp.join(root_path + "data", problem_name + '.txt')
    save_path = osp.join(root_path, save_name)
    if not osp.exists(save_path):
        record_dict = {"mtsp51": {"run_time": [], "optimal_length": [], "optimal_path": [], "minfun2val_per_round": []},
                       "mtsp100": {"run_time": [], "optimal_length": [], "optimal_path": [],
                                   "minfun2val_per_round": []},
                       "mtsp150": {"run_time": [], "optimal_length": [], "optimal_path": [],
                                   "minfun2val_per_round": []},
                       "pr76": {"run_time": [], "optimal_length": [], "optimal_path": [], "minfun2val_per_round": []},
                       "pr152": {"run_time": [], "optimal_length": [], "optimal_path": [], "minfun2val_per_round": []},
                       "pr226": {"run_time": [], "optimal_length": [], "optimal_path": [], "minfun2val_per_round": []}
                       }
        data = json.dumps(record_dict, indent=1)
        with open(save_path, "w") as f:
            f.write(data)

    with open(save_path, 'r', encoding='UTF-8') as f:
        record_dict = json.load(f)

    runtime, optimal_length, optimal_path, minfun1val_per_round = start(problem_path)
    record_dict[problem_name]["run_time"].append(runtime)
    record_dict[problem_name]["optimal_length"].append(optimal_length)
    record_dict[problem_name]["optimal_path"].append(optimal_path)
    record_dict[problem_name]["minfun2val_per_round"].append(minfun1val_per_round)

    data = json.dumps(record_dict, indent=1)
    with open(save_path, "w") as f:
        f.write(data)


parser = argparse.ArgumentParser()
parser.add_argument('-r', help='root path, note that data dir must in root path', required=True)
parser.add_argument('-p', help='problem name', required=True)
parser.add_argument('-o', help='result json file name', required=True)
args = parser.parse_args()
if __name__ == "__main__":
    try:
        run_and_save(args.r, args.p, args.o)
    except Exception as e:
        print(e)
