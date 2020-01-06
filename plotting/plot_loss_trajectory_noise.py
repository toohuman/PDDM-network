import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set(font_scale=1.2)

PERC_LOWER = 10
PERC_UPPER = 90

# states_set = [5, 10, 20, 30, 40, 50]
# agents_set = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
states_set = [10, 20, 30, 50]
agents_set = [10, 50, 100]
evidence_rates = [0.0, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]
er = 0.05
# Noise levels. None specifies no noise model, but required to use the same for-loop.
noise_levels = [0, 1, 5, 10, 20, 100]

result_directory = "../../results/test_results/pddm/"

closure = False
if closure:
    closure_string = "_no_closure"
else:
    closure_string = ""

iterations = [x for x in range(10001)]

for i, states in enumerate(states_set):
    for j, agents in enumerate(agents_set):

        print("{}, {}".format(states, agents))

        labels = ["{}:{} - {}".format(states, agents, noise) for noise in noise_levels]

        loss_results = np.array([[0.0 for z in iterations] for y in noise_levels])

        results_found = False

        for n, noise in enumerate(noise_levels):

            noise_input_string = ""
            noise_output_string = ""

            if noise is not None:
                noise_input_string += "_{:.3f}_nv".format(noise)
                noise_output_string += "_{}_nv".format(noise)

            if closure:
                file_name_parts = ["loss", agents, "agents", states, "states", "{:.3f}".format(er), "er", closure_string[1:], "{:.3f}".format(noise), "nv"]
            else:
                file_name_parts = ["loss", agents, "agents", states, "states", "{:.3f}".format(er), "er", "{:.3f}".format(noise), "nv"]
            file_ext = ".csv"
            file_name = "_".join(map(lambda x: str(x), file_name_parts)) + file_ext

            try:
                with open(result_directory + file_name, "r") as file:
                    iteration = 0
                    for line in file:
                        average_loss = np.average([float(x) for x in line.strip().split(",")])
                        loss_results[n][iteration] = average_loss
                        iteration += 1
                    for k in range(iteration, len(iterations)):
                        loss_results[n][k] = loss_results[n][iteration - 1]

                results_found = True
                print(loss_results[n])

            except FileNotFoundError:
                # If no file, just skip it.
                print(file_name)
                pass

        if not results_found:
            continue

        cmap = sns.cm.rocket
        c = [cmap(x/len(noise_levels)) for x in range(0, len(noise_levels))]
        for n, noise in enumerate(noise_levels):
            # if loss_results[n][0] == 0:
            #     continue
            if loss_results[n][0] == 0:
                continue
            ax = plt.plot(iterations, loss_results[n], linewidth = 2, color=c[n])
        plt.xlabel("Iterations")
        plt.ylabel("Average Loss")
        plt.title("{} agents, {} states".format(agents, states))
        plt.legend(noise_levels)
        if states == 10:
            plt.xlim((-30, 1100))
        # plt.show()
        plt.savefig("../../results/graphs/pddm/{}_agents_{}_states_{}_er{}.pdf".format(agents, states, er, closure_string))
        plt.clf()