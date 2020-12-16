import lzma
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pickle
import seaborn as sns; sns.set(font_scale=1.3)
import sys
sys.path.append("../utilities")
from results import *

PERC_LOWER = 10
PERC_UPPER = 90

states_set = [5, 10, 15, 20, 25]
agents_set = [100]
evidence_rates = [0.1]
evidence_strings = ["{:.2f}".format(x) for x in evidence_rates]
noise_values = [0.0, 5.0, 10.0, 100.0]
noise_strings = ["{:.0f}".format(x) for x in noise_values]
connectivity_value = 1.0

closure = ["", "_no_cl"]
closure_strings = ["With", "Without"]

result_directory = "../../results/test_results/pddm-network/"

for a, agents in enumerate(agents_set):
    for e, er in enumerate(evidence_rates):
        for c, cl in enumerate(closure):

            heatmap_results = np.array([[0.0 for x in states_set] for y in noise_values])

            data = None

            whole_evidence_set = True
            for n, noise in enumerate(reversed(noise_values)):
                for s, states in enumerate(states_set):

                    file_name_parts = [
                        "steady_state_error",
                        "{}a".format(agents),
                        "{}s".format(states),
                        "{:.2f}con".format(connectivity_value),
                        "{:.2f}er".format(er),
                        "{}nv{}".format(noise, cl)
                    ]
                    file_ext = ".csv"
                    file_name = "_".join(map(lambda x: str(x), file_name_parts)) + file_ext
                    # print(file_name)
                    try:
                        with open(result_directory + file_name, "r") as file:
                            # iteration = 0
                            # for line in file:
                            #     average_error = np.average([float(x) for x in line.strip().split(",")])

                            data = [[float(x) for x in line.rstrip('\n').split(',')] for line in file]
                    except FileNotFoundError:
                        print("MISSING: " + file_name)
                        heatmap_results[n][s] = 1.0
                        whole_evidence_set = False

                    data = sorted([np.average(x) for x in data])
                    # print(data)
                    # print(np.average(data))
                    # import time
                    # time.sleep(2)
                    heatmap_results[n][s] = np.average(data)

            # if data is None or not whole_evidence_set:
            #     continue

            # print("Average Error: {} states | {} agents | {:.2f} noise".format(states, agents, noise))
            # for c, cl in enumerate(closure):
            #     print("{}: ".format(closure_strings[c]), end=" ")
            #     for e, er in enumerate(evidence_rates):
            #         print("[{} er]: {:.3f}".format(er, results[c][e]), end=" ")
            #     print("")

            cmap = sns.cm.rocket_r
            ax = sns.heatmap(
                heatmap_results,
                # center=0,
                cmap=cmap,
                cbar=False,
                cbar_kws={"shrink": .75},
                xticklabels=states_set,
                yticklabels=list(reversed(noise_strings)),
                vmin=0, vmax=0.5,
                linewidths=.5,
                # annot=True,
                # annot_kws={"size": 8},
                # fmt=".2f",
                square=True
            )

            ax.set(xlabel=r'Options $n$', ylabel=r'Noise $\lambda$')
            plt.tight_layout()
            plt.savefig("../../results/graphs/pddm-network/hm_error_{}_agents_{:.0f}_er{}.pdf".format(agents, er, cl))
            plt.clf()