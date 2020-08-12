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
agents_set = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
evidence_rates = [0.01, 0.05, 0.1, 0.5, 1.0]
evidence_strings = ["{:.2f}".format(x) for x in evidence_rates]
noise_values = [0.0, 1.0, 2.5, 5.0, 7.5, 10.0, 100.0]
connectivity_value = 1.0

closure = ["", "_no_cl"]
closure_strings = ["With", "Without"]

result_directory = "../../results/test_results/pddm-network/"

for s, states in enumerate(states_set):
    for n, noise in enumerate(noise_values):
        for e, er in enumerate(evidence_rates):

            results = np.array([[0.0 for x in agents_set] for y in closure])
            lowers = np.array([[0.0 for x in agents_set] for y in closure])
            uppers = np.array([[0.0 for x in agents_set] for y in closure])

            data = None

            skip = True

            whole_agent_set = True
            for c, cl in enumerate(closure):
                for a, agents in enumerate(agents_set):

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
                        whole_agent_set = False

                    data = sorted([np.average(x) for x in data])
                    lowers[c][a] = data[PERC_LOWER - 1]
                    uppers[c][a] = data[PERC_UPPER - 1]
                    results[c][a] = np.average(data)

            if data is None or not whole_agent_set:
                continue

            print("Average Error: {} states | {:.2f} evidence rate | {:.2f} noise".format(states, er, noise))
            for c, cl in enumerate(closure):
                for a, agents in enumerate(agents_set):
                    print("[{}a]: {:.3f}".format(agents, results[c][a]), end=" ")
                print("")

            # flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
            # sns.set_palette(sns.color_palette(flatui))
            sns.set_palette("rocket", len(closure))
            for c, cl in enumerate(closure):
                ax = sns.lineplot(agents_set, results[c], linewidth = 2, color=sns.color_palette()[c], label=closure_strings[c])
                plt.fill_between(agents_set, lowers[c], uppers[c], facecolor=sns.color_palette()[c], edgecolor="none", alpha=0.3, antialiased=True)
            plt.axhline(expected_error(noise, states), color="red", linestyle="dotted", linewidth = 2)
            plt.xlabel("Agents")
            plt.ylabel("Average Error")
            plt.ylim(-0.01, 0.425)
            # if noise == 0:
            #     plt.ylim(-0.05, 0.05)
            # elif noise == 0.5:
            #     plt.ylim(0.0, 1.0)
            # else:
            #     if connectivity_value == 1.0:
            #         plt.ylim(-0.01, noise + (noise * 0.3))
            #     elif connectivity_value == 0.0:
            #         plt.ylim(noise - 0.05, noise + 0.05)
            # plt.title("Average error | {} states, {} er, {} noise".format(states, er, noise))

            # ax.get_legend().remove()

            # import pylab
            # fig_legend = pylab.figure(figsize=(1,2))
            # pylab.figlegend(*ax.get_legend_handles_labels(), loc="upper left", ncol=len(evidence_strings))
            # fig_legend.show()
            # plt.show()

            # import time
            # time.sleep(10)

            plt.tight_layout()
            # Complete graph
            if connectivity_value == 1.0:
                plt.savefig("../../results/graphs/pddm-network/error_comps_{}_states_{:.2f}_er_{:.2f}_noise.pdf".format(states, er, noise))
            # Evidence-only graph
            elif connectivity_value == 0.0:
                plt.savefig("../../results/graphs/pddm-network/error_comps_ev_only_{}_states_{:.2f}_er_{:.2f}_noise.pdf".format(states, er, noise))
            plt.clf()