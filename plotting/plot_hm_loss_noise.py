import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set()

PERC_LOWER = 10
PERC_UPPER = 90

states_set = [10, 20, 30]
agents_set = [10, 50, 100]
noise_values = [0, 1, 5, 10, 20, 100]
er = 0.05

result_directory = "../../results/test_results/pddm-network/"

for j, agents in enumerate(agents_set):
    heatmap_results = np.array([[0.0 for x in noise_values] for y in states_set])
    labels = [["" for x in noise_values] for y in states_set]

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

                steady_state_results = [float(x) for x in steady_state_results.strip().split(",")]

                average_loss = np.average(steady_state_results)

                heatmap_results[i][n] = average_loss

            except FileNotFoundError:
                # Add obvious missing entry into final results array here
                heatmap_results[i][n] = 1.0

    print(heatmap_results)
    print(labels)
    # cmap = sns.cubehelix_palette(8, start=3.3, rot=0.33, dark=0, light=.96, hue=1.8, as_cmap=True)
    # cmap = sns.cubehelix_palette(8, start=2.4, rot=0.68, dark=0.08, light=.96, hue=1, as_cmap=True)
    # cmap = cm.get_cmap('magma') #'Greys_r'
    cmap = sns.cm.rocket_r
    ax = sns.heatmap(
        heatmap_results,
        # center=0,
        cmap=cmap,
        cbar_kws={"shrink": .75},
        xticklabels=noise_values,
        yticklabels=list(reversed(states_set)),
        vmin=0, vmax=1,
        linewidths=.5,
        square=True
    )
    plt.title("{} agents, {} evidence rate".format(agents, er))
    ax.set(xlabel='Noise value', ylabel='No. of States')
    # plt.show()
    plt.savefig("../../results/graphs/pddm-network/{}_agents_hm_{}_er_noise.pdf".format(agents, states, er))
    plt.clf()