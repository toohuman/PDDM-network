import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set(font_scale=1.3)
import sys
sys.path.append("../utilities")
from results import *

PERC_LOWER = 10
PERC_UPPER = 90

states_set = [10, 20]
agents_set = [10, 100]
evidence_rates = [0.01, 0.05, 0.1, 0.5, 1.0]
evidence_strings = ["{:.2f}".format(x) for x in evidence_rates]
noise_levels = [0.0, 1.0, 2.5, 5.0, 7.5, 10.0, 100.0]
connectivity_values = [0.0, 0.01, 0.02, 0.05, 0.1, 0.5, 1.0]
connectivity_strings = ["{:.2f}".format(x) for x in connectivity_values]

iterations = [x for x in range(10001)]
conn = 1.0

closure = True
if closure is False:
    closure = "_no_cl"
else:
    closure = ""

result_directory = "../../results/test_results/pddm-network/"

for s, states in enumerate(states_set):
    for n, noise in enumerate(noise_levels):
        for a, agents in enumerate(agents_set):

            results = np.array([[0.0 for x in iterations] for y in evidence_rates])
            lowers = np.array([[0.0 for x in iterations] for y in evidence_rates])
            uppers = np.array([[0.0 for x in iterations] for y in evidence_rates])
            data = None

            for e, er in enumerate(evidence_rates):

                file_name_parts = [
                    "error",
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

                        data = [[float(x) for x in line.rstrip('\n').split(',')] for line in file]

                    for i, tests in enumerate(data):
                        sorted_data = sorted(tests)
                        lowers[e][i] = sorted_data[PERC_LOWER - 1]
                        uppers[e][i] = sorted_data[PERC_UPPER - 1]
                        results[e][i] = np.average(tests)

                except FileNotFoundError:
                    print("MISSING: " + file_name)

            if data is None:
                continue

            # print(error_results)
            import math
            convergence_times = ["" for x in evidence_rates]
            steady_state_threshold = 100
            for e, er_results in enumerate(results):
                convergence_counter = 0
                prev_iteration = -1
                for i, iteration in enumerate(er_results):
                    if math.isclose(iteration, 0) or convergence_counter == steady_state_threshold:
                        if convergence_counter == steady_state_threshold:
                            i -= steady_state_threshold
                        convergence_times[e] += "{} t [converged @ {}]".format(i, iteration)
                        break
                    elif i == len(er_results) - 1:
                        convergence_times[e] = -1
                    elif math.isclose(iteration, prev_iteration):
                        convergence_counter += 1
                    else:
                        convergence_counter = 0
                    prev_iteration = iteration


            print("{} states | {} agents | {:.2f} noise - E(error) = {:.2f}".format(states, agents, noise, expected_error(noise, states)))
            for e, er in enumerate(evidence_rates):
                print("   [{:.2f} er]: {}".format(er, convergence_times[e]))


            for _ in range(2):
                sns.set_palette("rocket", len(evidence_rates))
                for e, er in enumerate(evidence_rates):
                    ax = sns.lineplot(iterations, results[e], linewidth = 2, color=sns.color_palette()[e], label=evidence_strings[e])
                    plt.fill_between(iterations, lowers[e], uppers[e], facecolor=sns.color_palette()[e], edgecolor="none", alpha=0.3, antialiased=True)

                plt.axhline(expected_error(noise, states), color="red", linestyle="dotted", linewidth = 2)
                plt.xlabel(r'Time $t$')
                plt.ylabel("Average Error")
                plt.ylim(-0.01, 0.525)
                plt.xlim(0, 4000)
                # plt.title("Average error | {} states, {} er, {} noise".format(states, er, noise))

                ax.get_legend().remove()

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
                    plt.savefig("../../results/graphs/pddm-network/error_trajectory_{}_agents_{}_states_{:.2f}_noise{}.pdf".format(agents, states, noise, closure))
                # Evidence-only graph
                elif conn == 0.0:
                    plt.savefig("../../results/graphs/pddm-network/error_trajectory_ev_only_{}_agents_{}_states_{:.2f}_noise{}.pdf".format(agents, states, noise, closure))
                plt.clf()