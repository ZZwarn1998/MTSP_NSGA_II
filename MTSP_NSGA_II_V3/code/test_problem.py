from ga import GA
import numpy as np
import json
import matplotlib.pyplot as plt

if __name__ == "__main__":

    record_dict = {}

    for data_name in ["mtsp51", "mtsp100", "mtsp150", "pr76", "pr152", "pr226"]:
        tmp_dict = {}
        run_time_all = []
        optimal_length_all = []
        optimal_path_all = []
        minfun1val_per_round_all = []

        for i in range(30):
            ga = GA(data_name, 5, 100, 200, 0.2)
            runtime, optimal_length, optimal_path, minfun1val_per_round = ga.solve()
            run_time_all.append(runtime)
            optimal_length_all.append(optimal_length)
            optimal_path_all.append(optimal_path)
            minfun1val_per_round_all.append(minfun1val_per_round)
        tmp_dict = {"run_time": run_time_all,
                    "optimal_length": optimal_length_all,
                    "optimal_path": optimal_path_all,
                    "minfun2val_per_round": minfun1val_per_round_all}
        record_dict.update({data_name: tmp_dict})

    data = json.dumps(record_dict, indent=1)
    with open("./record.json", "w") as f:
        f.write(data)
