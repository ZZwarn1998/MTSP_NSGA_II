import numpy as np
import pandas as pd
import json
from scipy import stats


def summary_data(base_run_data, ous_run_data):
    data_name = ["mtsp51", "mtsp100", "mtsp150", "pr76", "pr152", "pr226"]
    for run_data_dict in [base_run_data, ous_run_data]:
        row_list = []
        for name in data_name:
            each_dict = run_data_dict[name]
            optimal_length = each_dict["optimal_length"]
            times = each_dict["run_time"]
            avg = np.mean(optimal_length)
            std = np.std(optimal_length)
            min_solution = min(optimal_length)
            max_solution = max(optimal_length)
            avg_time = np.mean(times)
            row_list.append([name, avg, std, min_solution, max_solution, avg_time])
        df = pd.DataFrame(columns=["problem", "avg", "std", "min", "max", "time"], data=row_list)
        pd.set_option('display.max_columns', None)
        print(df)


def wilconxon_rank_test(run_data_1, run_data_2):
    data_name = ["mtsp51", "mtsp100", "mtsp150", "pr76", "pr152", "pr226"]
    for name in data_name:
        optimal_solution_1 = run_data_1[name]["optimal_length"]
        optimal_solution_2 = run_data_2[name]["optimal_length"]
        print(stats.wilcoxon(optimal_solution_1, optimal_solution_2, alternative='two-sided'))


if __name__ == "__main__":
    with open("baseline_run_data.json", 'r', encoding='UTF-8') as f:
        base = json.load(f)
    with open("ours_run_data.json", 'r', encoding='UTF-8') as f:
        ours = json.load(f)
    # summary_data(base, ours)
    wilconxon_rank_test(base, ours)
