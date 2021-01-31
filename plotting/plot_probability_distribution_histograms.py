import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import seaborn as sns; sns.set(font_scale=1.3)
import sys
sys.path.append("../utilities")
from results import *

states_set = [10]
agents_set = [100]
evidence_rates = [0.01, 0.05, 0.1, 0.5, 1.0]
evidence_strings = ["{:.2f}".format(x) for x in evidence_rates]
noise_levels = [0.0, 0.1, 0.2, 0.3, 0.4]
connectivity_values = [0.0, 0.01, 0.02, 0.05, 0.1, 0.5, 1.0]
connectivity_strings = ["{:.2f}".format(x) for x in connectivity_values]

iterations = [x for x in range(10001)]
conn = 1.0

agent_type = "probabilistic" # probabilistic | average

closure = False
if closure is False:
    closure = "_no_cl"
else:
    closure = ""

result_directory = "../../results/test_results/pddm-network/{}/".format(agent_type)


for s, states in enumerate(states_set):
    for n, noise in enumerate(noise_levels):
        for a, agents in enumerate(agents_set):
            for e, er in enumerate(evidence_rates):

                results = np.array([[] for x in range(states)])
                data = None

                file_name_parts = [
                    "steady_state_probabilities",
                    "{}a".format(agents),
                    "{}s".format(states),
                    "{:.2f}con".format(conn),
                    "{:.2f}er".format(er),
                    "{}nv{}".format(noise, closure)
                ]
                file_ext = ".csv"
                file_name = "_".join(map(lambda x: str(x), file_name_parts)) + file_ext
                # print(file_name)

                try:
                    with open(result_directory + file_name, "r") as file:
                        # iteration = 0
                        # for line in file:
                        #     average_error = np.average([float(x) for x in line.strip().split(",")])

                        data = np.array([[[float(x) for x in y.split(',')] for y in line.lstrip('[').rstrip(']\n').split('],[')] for line in file])

                    restructured_data = data.reshape((data.shape[0]*data.shape[1]), data.shape[2])

                    df = pd.DataFrame(data=restructured_data)


                except FileNotFoundError:
                    print("MISSING: " + file_name)

                if data is None:
                    continue

                sns.set_palette("rocket", states)
                # for i in range(states):
                #     ax = sns.histplot(data=df[i], bins=20, color=sns.color_palette()[i], label=r'$p(s_{})$'.format(i))

                ax = sns.histplot(data=df, bins=20, color=sns.color_palette(), common_bins=True)

                # plt.axhline(expected_error(noise, states), color="red", linestyle="dotted", linewidth = 2)
                plt.xlabel(r'Probability')
                # plt.ylim(-0.01, 100)
                # plt.xlim(-0.01, 1.01)
                plt.title("Probability distributions | {} states, {} er, {} noise".format(states, er, noise))

                # ax.get_legend().remove()

                # import pylab
                # fig_legend = pylab.figure(figsize=(1,2))
                # pylab.figlegend(*ax.get_legend_handles_labels(), loc="upper left", ncol=len(connectivity_strings))
                # fig_legend.show()
                # plt.show()

                # import time
                # time.sleep(10)

                plt.tight_layout()
                # Complete graph
                if conn == 1.0:
                    plt.savefig("../../results/graphs/pddm-network/{}/distribution_histograms_{}_agents_{}_states_{:.2f}_er_{:.2f}_noise{}.pdf".format(agent_type, agents, states, er, noise, closure))
                # Evidence-only graph
                elif conn == 0.0:
                    plt.savefig("../../results/graphs/pddm-network/{}/distribution_histograms_ev_only_{}_agents_{}_states_{:.2f}_er_{:.2f}_noise{}.pdf".format(agent_type, agents, states, er, noise, closure))
                plt.clf()