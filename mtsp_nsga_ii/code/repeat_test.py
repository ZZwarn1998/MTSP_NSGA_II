from ga import GA
import json

"""This is the file to run repeat test experiment"""

if __name__ == "__main__":
    problem_name_list = ["mtsp51", "mtsp100", "mtsp150", "pr76", "pr152", "pr226"]
    num_travellers = 5
    population_size = 100
    generations = 200
    mutation_rate = 0.2
    repeat_times = 30

    record_dict = {}
    for data_name in problem_name_list:
        tmp_dict = {}
        run_time_all = []
        optimal_length_all = []
        optimal_path_all = []
        minfun1val_per_round_all = []

        for i in range(repeat_times):
            ga = GA(data_name, num_travellers, population_size, generations, mutation_rate)
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
    with open("./ours_run_data.json", "w") as f:
        f.write(data)
