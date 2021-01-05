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

states_set = [10, 20]
agents_set = [100]
fusion_rates = [1, 5, 10, 20, 30, 40, 50]
fusion_strings = ["{:.2f}".format(x/100) for x in fusion_rates]
evidence_rates = [0.01, 0.05, 0.1, 0.5, 1.0]
evidence_strings = ["{:.2f}".format(x) for x in evidence_rates]
noise_values = [0.0, 1.0, 2.5, 5.0, 7.5, 10.0, 100.0]
connectivity_value = 1.0

closure = ["", "_no_cl"]
closure_strings = ["With", "Without"]

result_directory = "../../results/test_results/pddm-network/"

for s, states in enumerate(states_set):
    for a, agents in enumerate(agents_set):
        for n, noise in enumerate(noise_values):
            for c, cl in enumerate(closure):

                heatmap_results = np.array([[0.0 for x in fusion_rates] for y in evidence_rates])

                data = None

                whole_evidence_set = True
                for e, er in enumerate(reversed(evidence_rates)):
                    for f, fr in enumerate(fusion_rates):

                        file_name_parts = [
                            "steady_state_error",
                            "{}a".format(agents),
                            "{}s".format(states),
                            "{:.2f}con".format(connectivity_value),
                            "{:.2f}er".format(er),
                            "{}nv".format(noise),
                            "{}fr{}".format(fr, cl)
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
                            heatmap_results[e][f] = 1.0
                            whole_evidence_set = False

                        if data is None:
                            continue

                        data = sorted([np.average(x) for x in data])
                        # print(data)
                        # print(np.average(data))
                        # import time
                        # time.sleep(2)
                        heatmap_results[e][f] = np.average(data)

                if data is None:# or not whole_evidence_set:
                    continue

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
                    cbar=True,
                    cbar_kws={"shrink": .75},
                    xticklabels=fusion_rates,
                    yticklabels=list(reversed(evidence_strings)),
                    vmin=0, vmax=0.5,
                    linewidths=.5,
                    # annot=True,
                    # annot_kws={"size": 8},
                    # fmt=".2f",
                    square=True
                )

                ax.set(xlabel='Fusion rate', ylabel='Evidence rate')
                plt.tight_layout()
                plt.savefig("../../results/graphs/pddm-network/hm_error_ev_fr_{}_states_{}_agents_{:.2f}_noise{}.pdf".format(states, agents, noise, cl))
                plt.clf()