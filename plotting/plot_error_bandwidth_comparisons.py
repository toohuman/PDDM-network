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

PERC_LOWER = 5  # 10
PERC_UPPER = 45 # 90

states_set = [10]
agents_set = [100]
evidence_rates = [0.01, 0.05, 0.1, 0.5, 1.0]
evidence_strings = ["{:.2f}".format(x) for x in evidence_rates]
noise_levels = [0.0, 1.0, 2.5, 5.0, 7.5, 10.0, 100.0]
connectivity_values = [0.0, 0.01, 0.02, 0.05, 0.1, 0.5, 1.0]
connectivity_strings = ["{:.2f}".format(x) for x in connectivity_values]

iterations = [x for x in range(10001)]
conn = 1.0

closure = ["", "_no_cl"]
closure_strings = ["With", "Without"]
cl = closure[1]

bandwidth = ["", "bandwidth/"]
bandwidth_strings = ["Standard", "Limited"]

result_directory = "../../results/test_results/pddm-network/"


for s, states in enumerate(states_set):
    for n, noise in enumerate(noise_levels):
        for a, agents in enumerate(agents_set):
            for e, er in enumerate(evidence_rates):

                results = np.array([[0.0 for x in iterations] for y in bandwidth])
                lowers = np.array([[0.0 for x in iterations] for y in bandwidth])
                uppers = np.array([[0.0 for x in iterations] for y in bandwidth])

                data = None

                skip = True

                whole_agent_set = True
                for b, bw in enumerate(bandwidth):

                    file_name_parts = [
                        "error",
                        "{}a".format(agents),
                        "{}s".format(states),
                        "{:.2f}con".format(conn),
                        "{:.2f}er".format(er),
                        "{}nv{}".format(noise, cl)
                    ]
                    file_ext = ".csv"
                    file_name = "_".join(map(lambda x: str(x), file_name_parts)) + file_ext
                    # print(file_name)
                    try:
                        with open(result_directory + bw + file_name, "r") as file:

                            data = [[float(x) for x in line.rstrip('\n').split(',')] for line in file]

                    except FileNotFoundError:
                        print("MISSING: " + bw + file_name)
                        whole_agent_set = False

                    for i, tests in enumerate(data):
                        sorted_data = sorted(tests)
                        if bw == "":
                            lowers[b][i] = sorted_data[PERC_LOWER*2 - 1]
                            uppers[b][i] = sorted_data[PERC_UPPER*2 - 1]
                        else:
                            lowers[b][i] = sorted_data[PERC_LOWER - 1]
                            uppers[b][i] = sorted_data[PERC_UPPER - 1]
                        results[b][i] = np.average(tests)

                if data is None or not whole_agent_set:
                    continue

                print("Average Error: {} states | {:.2f} evidence rate | {:.2f} noise".format(states, er, noise))
                for b, bw in enumerate(bandwidth):
                    print("{}: ".format(bandwidth_strings[b]), end=" ")
                    print("{:.3f} @ss".format(results[b][-1]))

                # flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
                # sns.set_palette(sns.color_palette(flatui))
                sns.set_palette("rocket", len(bandwidth))
                for b, bw in enumerate(bandwidth):
                    ax = sns.lineplot(x=iterations, y=results[b], linewidth = 2, color=sns.color_palette()[b], label=bandwidth_strings[b])
                    plt.fill_between(iterations, lowers[b], uppers[b], facecolor=sns.color_palette()[b], edgecolor="none", alpha=0.3, antialiased=True)
                plt.axhline(expected_error(noise, states), color="red", linestyle="dotted", linewidth = 2)
                plt.xlabel(r'Time $t$')
                plt.ylabel("Average Error")
                plt.ylim(-0.01, 0.525)
                plt.xlim(0, 10000)

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
                if conn == 1.0:
                    plt.savefig("../../results/graphs/pddm-network/bandwidth/error_comps_{}_agents_{}_states_{:.2f}_er_{:.2f}_noise.pdf".format(agents, states, er, noise))
                # Evidence-only graph
                elif conn == 0.0:
                    plt.savefig("../../results/graphs/pddm-network/bandwidth/error_comps_ev_only_{}_agents_{}_states_{:.2f}_er_{:.2f}_noise.pdf".format(agents, states, er, noise))
                plt.clf()