import seaborn as sb
import json
import pandas as pd
import matplotlib.pyplot as plt


def plot_figure(data_name, baseline_run_data, ours_run_data, start_generations):
    row_list = []
    for summary in [(baseline_run_data, "baseline"), (ours_run_data, "ours")]:
        for round_data in summary[0][data_name]["minfun2val_per_round"]:
            for generation, obj in enumerate(round_data):
                row_list.append([summary[1], generation + 1, obj])

    df = pd.DataFrame(columns=["methods", "generations", "obj"], data=row_list)
    new_df = df[df["generations"] > start_generations]
    sb.lineplot(data=new_df, x="generations", hue="methods", y="obj", ci="sd")
    plt.yticks(rotation=30)
    plt.title(data_name)


def plot_all_figure(baseline_run_data, ours_run_data, start_generations):
    fig = plt.figure(figsize=(20, 10))
    data_name = ["mtsp51", "mtsp100", "mtsp150", "pr76", "pr152", "pr226"]
    for i in range(6):
        fig.add_subplot(2, 3, i + 1)
        plot_figure(data_name[i], baseline_run_data, ours_run_data, start_generations)
    plt.savefig(fname="unite.svg", format="svg")


if __name__ == "__main__":
    with open("baseline_run_data.json", 'r', encoding='UTF-8') as f:
        base = json.load(f)
    with open("ours_run_data.json", 'r', encoding='UTF-8') as f:
        ours = json.load(f)
    plot_all_figure(base, ours, 2)
