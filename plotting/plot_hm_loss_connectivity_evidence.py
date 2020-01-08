import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set()

PERC_LOWER = 10
PERC_UPPER = 90

agents_set = [100]
states_set = [10]
evidence_rates = [0.0, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
evidence_strings = ["{:.3f}".format(x) for x in evidence_rates]
noise_values = [0.0, 1.0, 5.0, 10.0, 20.0, 100.0]
connectivity_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
connectivity_strings = ["{:.1f}".format(x) for x in connectivity_values]

result_directory = "../../results/test_results/pddm-network/"

for a, agents in enumerate(agents_set):
    for s, states in enumerate(states_set):
        for n, noise in enumerate(noise_values):

            heatmap_results = np.array([[0.0 for x in connectivity_values] for y in evidence_rates])
            labels = [["" for x in connectivity_values] for y in evidence_rates]

            skip = True

            for e, er in enumerate(reversed(evidence_rates)):
                for c, con in enumerate(connectivity_values):

                    file_name_parts = ["loss", agents, "agents", states, "states", "{:.3f}".format(noise), "nv", "{:.3f}".format(er), "er", "{:.1f}".format(con), "con"]
                    file_ext = ".csv"
                    file_name = "_".join(map(lambda x: str(x), file_name_parts)) + file_ext
                    print(file_name)

                    labels[s][n] = "{} A : {} S : {} N".format(agents, states, noise)

                    steady_state_results = []
                    average_loss = 0.0

                    try:
                        with open(result_directory + file_name, "r") as file:
                            for line in file:
                                steady_state_results = line
                        print(file_name)

                        steady_state_results = [float(x) for x in steady_state_results.strip().split(",")]

                        average_loss = np.average(steady_state_results)

                        heatmap_results[s][n] = average_loss

                        skip = False

                    except FileNotFoundError:
                        # Add obvious missing entry into final results array here
                        heatmap_results[s][n] = 1.0

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
        yticklabels=list(reversed(evidence_strings)),
        vmin=0, vmax=1,
        linewidths=.5,
        annot=True,
        annot_kws={"size": 10},
        fmt=".2f",
        square=True
    )
    plt.title("Average loss | {} agents, {} states, {} noise".format(agents, states, noise))
    ax.set(xlabel='Connectivity', ylabel='Evidence rate')
    # plt.show()
    plt.savefig("../../results/graphs/pddm-network/hm_loss_{}_agents_{}_states_{}_noise_er_con.pdf".format(agents, states, noise), bbox_inches="tight")
    plt.clf()