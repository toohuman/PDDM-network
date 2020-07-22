import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set()

PERC_LOWER = 10
PERC_UPPER = 90

states_set = [5, 10, 20, 30, 40, 50]
agents_set = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
evidence_rates = [0.0, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]
er = 0.05

result_directory = "../../results/test_results/pddm-network/"

heatmap_results = np.array([[0.0 for x in agents_set] for y in states_set])
labels = [["" for x in agents_set] for y in states_set]

for i, states in enumerate(reversed(states_set)):
    for j, agents in enumerate(agents_set):
        file_name_parts = ["error", agents, "agents", states, "states", "{:.3f}".format(er), "er"]
        file_ext = ".csv"
        file_name = "_".join(map(lambda x: str(x), file_name_parts)) + file_ext

        steady_state_results = []

        labels[i][j] = "{}:{}".format(states, agents)

        try:
            with open(result_directory + file_name, "r") as file:
                for line in file:
                    steady_state_results = line

            steady_state_results = [float(x) for x in steady_state_results.strip().split(",")]

            average_error = np.average(steady_state_results)

            heatmap_results[i][j] = average_error

        except FileNotFoundError:
            # Add obvious missing entry into final results array here
            heatmap_results[i][j] = 1.0

print(heatmap_results)
print(labels)
cmap = sns.cm.rocket_r
ax = sns.heatmap(
    heatmap_results,
    # center=0,
    cmap=cmap,
    cbar_kws={"shrink": .75},
    xticklabels=agents_set,
    yticklabels=list(reversed(states_set)),
    vmin=0, vmax=1,
    linewidths=.5,
    square=True
)
ax.set(xlabel='No. of Agents', ylabel='No. of States')
plt.show()