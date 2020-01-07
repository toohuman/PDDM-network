import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set()

PERC_LOWER = 10
PERC_UPPER = 90

agents_set = [100]
states_set = [5, 10, 20, 50, 100]
states_set_formatted = ["5x5", "10x10", "20x20", "50x50", "100x100"]
evidence_rates = [0.0, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
noise_values = [0.0, 1.0, 5.0, 10.0, 20.0, 100.0]
connectivity_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

result_directory = "../../results/test_results/pddm-network/"

for j, agents in enumerate(agents_set):
    heatmap_results = np.array([[0.0 for x in noise_values] for y in states_set])
    labels = [["" for x in noise_values] for y in states_set]

    skip = True

    for i, states in enumerate(reversed(states_set)):
        for n, noise in enumerate(noise_values):
            file_name_parts = ["loss", agents, "agents", states, "states", "{:.3f}".format(er), "er", "{:.3f}".format(noise), "nv"]
            file_ext = ".csv"
            file_name = "_".join(map(lambda x: str(x), file_name_parts)) + file_ext

            steady_state_results = []

            labels[i][n] = "{}:{}".format(states, noise)

            try:
                with open(result_directory + file_name, "r") as file:
                    for line in file:
                        steady_state_results = line
                print(file_name)

                steady_state_results = [float(x) for x in steady_state_results.strip().split(",")]

                average_loss = np.average(steady_state_results)

                heatmap_results[i][n] = average_loss

                skip = False

            except FileNotFoundError:
                # Add obvious missing entry into final results array here
                heatmap_results[i][n] = 1.0

    if skip:
        continue

    print(heatmap_results)
    print(labels)
    cmap = sns.cm.rocket_r
    ax = sns.heatmap(
        heatmap_results,
        # center=0,
        cmap=cmap,
        cbar_kws={"shrink": .75},
        xticklabels=noise_values,
        yticklabels=list(reversed(states_set_formatted)),
        vmin=0, vmax=1,
        linewidths=.5,
        annot=True,
        annot_kws={"size": 10},
        fmt=".2f",
        square=True
    )
    plt.title("Average loss | {} agents, {} evidence rate".format(agents, er))
    ax.set(xlabel='Noise value', ylabel='No. of States')
    # plt.show()
    plt.savefig("../../results/graphs/pddm-network/loss_hm_{}_agents_{}-{}_states_noisy{}{}.pdf".format(agents, states_set[0], states_set[-1], partition_str, exploration_str), bbox_inches="tight")
    plt.clf()