import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set()

PERC_LOWER = 10
PERC_UPPER = 90

states_set = [5, 10, 20, 30, 40, 50]
agents_set = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
evidence_rates = [0.0, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]
er = 0.01
# Noise levels. None specifies no noise model, but required to use the same for-loop.
noise_levels = [0, 1, 5, 10, 20, 100]
noise_levels = [None]

result_directory = "../../results/test_results/pddm/"

iterations = [x for x in range(10000)]

for noise in noise_levels:

    noise_input_string, noise_output_string = ""
    if noise is not None:
        noise_input_string += "_{:.3f}_nv".format(noise)
        noise_output_string += "_{}_nv".format(noise)

    loss_results = np.array([[[0.0 for z in iterations] for y in agents_set] for x in states_set])
    labels = [["" for x in agents_set] for y in states_set]

    for i, states in enumerate(states_set):
        for j, agents in enumerate(agents_set):
            file_name_parts = ["loss", agents, "agents", states, "states", "{:.3f}".format(er), "er"]
            file_ext = ".csv"
            file_name = "_".join(map(lambda x: str(x), file_name_parts)) + file_ext

            steady_state_results = []

            labels[i][j] = "{}:{}".format(states, agents)

            try:
                with open(result_directory + file_name, "r") as file:
                    iteration = 0
                    for line in file:
                        average_loss = np.average([float(x) for x in line.strip().split(",")])

                        loss_results[i][j][iteration] = average_loss
                        iteration += 1
                    for k in range(iteration, len(iterations)):
                        loss_results[i][j][k] = loss_results[i][j][iteration - 1]

            except FileNotFoundError:
                # If no file, just skip it.
                pass

    print(loss_results)
    print(labels)
    cmap = sns.cm.rocket
    c = [cmap(x/len(states_set)) for x in range(0, len(states_set))]
    for j, agents in enumerate(agents_set):
        for i, states in enumerate(states_set):
            if loss_results[i][j][0] == 0:
                continue
            ax = plt.plot(iterations, loss_results[i][j], linewidth = 2, color=c[i])
        plt.xlabel("Iterations")
        plt.ylabel("Average Loss")
        plt.title("{} agents".format(agents))
        plt.legend(states_set)
        # plt.show()
        plt.savefig("../../results/graphs/pddm/{}_agents_{}_er.pdf".format(agents, er))
        plt.clf()