import lzma
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pickle
import seaborn as sns; sns.set(font_scale=1.3)
import sys
sys.path.append("../utilities")
from preferences import *
from results import *

states_set = [5, 10, 15, 20, 25]
distances_set = [
    [state for state in range(1, states)]
    for states in states_set
]
print(distances_set)
noise_values = [0.0, 1.0, 2.5, 5.0, 7.5, 10.0, 100.0]
noise_strings = ["{:.1f}".format(x) for x in noise_values]
connectivity_value = 1.0

closure = False
if closure is False:
    closure = "_no_cl"
else:
    closure = ""

result_directory = "../../results/test_results/pddm-network/"

for s, states in enumerate(states_set):

    results = np.array([[0.0 for x in distances_set[s]] for y in noise_values])

    for n, noise in enumerate(noise_values):
        for d, distance in enumerate(distances_set[s]):

            results[n][d] = comparison_error(distance / states, noise)

    # print("Average Error: {} states | {:.2f} noise".format(states, noise))
    # for n, noise in enumerate(noise_values):
    #     print("   [{}n]:  ".format(noise), end="")
    #     for d, distance in enumerate(distances_set[s]):
    #         print("[{}d]: {:.3f}".format(distance, results[n][d]), end=" ")
    #     print("")

    # flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    # sns.set_palette(sns.color_palette(flatui))
    sns.set_palette("rocket_r", len(noise_values) + 1)
    for n, noise in enumerate(noise_values):
        ax = sns.lineplot(distances_set[s], results[n], linewidth = 2, color=sns.color_palette()[n], label=noise_strings[n])
    plt.xlabel(r'Option Distance $|i - j|$')
    plt.ylabel(r'Comparison Error $C_\lambda$')
    plt.ylim(-0.025, 0.501)
    if states / 2 < 10:
        plt.xticks(distances_set[s])
    else:
        plt.xticks([x for x in distances_set[s][::2]])
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
        plt.savefig("../../results/graphs/pddm-network/comparison_errors_{}_states.pdf".format(states))
    plt.clf()