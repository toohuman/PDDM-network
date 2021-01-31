import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns; sns.set(font_scale=1.3)
import sys
sys.path.append("../utilities")
from results import *

PERC_LOWER = 10
PERC_UPPER = 100

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

                results = np.array([[0.0 for x in range(states - 1)] for y in iterations])
                lowers = np.array([[0.0 for x in range(states - 1)] for y in iterations])
                uppers = np.array([[0.0 for x in range(states - 1)] for y in iterations])
                data = None

                file_name_parts = [
                    "preferences",
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

                    for t, test in enumerate(data):
                        for i in range(states - 1):
                            sorted_data = sorted(test[:,i])
                            lowers[t][i] = sorted_data[PERC_LOWER - 1]
                            uppers[t][i] = sorted_data[PERC_UPPER - 1]
                            results[t][i] = np.average(sorted_data)

                except FileNotFoundError:
                    print("MISSING: " + file_name)                # import math
                # convergence_times = ["" for x in evidence_rates]
                # steady_state_threshold = 100
                # for e, er_results in enumerate(results):
                #     convergence_counter = 0
                #     prev_iteration = -1
                #     for i, iteration in enumerate(er_results):
                #         if math.isclose(iteration, 0) or convergence_counter == steady_state_threshold:
                #             if convergence_counter == steady_state_threshold:
                #                 i -= steady_state_threshold
                #             convergence_times[e] += "{} t [converged @ {}]".format(i, iteration)
                #             break
                #         elif i == len(er_results) - 1:
                #             convergence_times[e] = "-1 t [ended @ {}]".format(iteration)
                #         elif math.isclose(iteration, prev_iteration):
                #             convergence_counter += 1
                #         else:
                #             convergence_counter = 0
                #         prev_iteration = iteration

                if data is None:
                    continue

                # print(error_results)
                # import math
                # convergence_times = ["" for x in evidence_rates]
                # steady_state_threshold = 100
                # for e, er_results in enumerate(results):
                #     convergence_counter = 0
                #     prev_iteration = -1
                #     for i, iteration in enumerate(er_results):
                #         if math.isclose(iteration, 0) or convergence_counter == steady_state_threshold:
                #             if convergence_counter == steady_state_threshold:
                #                 i -= steady_state_threshold
                #             convergence_times[e] += "{} t [converged @ {}]".format(i, iteration)
                #             break
                #         elif i == len(er_results) - 1:
                #             convergence_times[e] = "-1 t [ended @ {}]".format(iteration)
                #         elif math.isclose(iteration, prev_iteration):
                #             convergence_counter += 1
                #         else:
                #             convergence_counter = 0
                #         prev_iteration = iteration


                # print("{} states | {} agents | {:.2f} noise, | {:.2f} er".format(states, agents, noise, evidence))
                # print("   [{:.2f} er]: {}".format(er, convergence_times[e]))


                # for _ in range(2):    # This was to fix a weird drawing bug in matplotlib
                sns.set_palette("rocket", states - 1)
                for i, state in enumerate(range(states - 1, 0, -1)):
                    ax = sns.lineplot(x=iterations, y=results[:,i], linewidth = 2, color=sns.color_palette()[i], label=r'$({}, {})$'.format(state, state - 1))
                    # plt.fill_between(iterations, lowers[:,i], uppers[:,i], facecolor=sns.color_palette()[i], edgecolor="none", alpha=0.3, antialiased=True)

                # plt.axhline(expected_error(noise, states), color="red", linestyle="dotted", linewidth = 2)
                plt.xlabel(r'Time $t$')
                plt.ylabel("Proportion of population")
                plt.ylim(-0.01, 1)
                plt.xlim(0, 3000)
                plt.title("Average error | {} states, {} er, {} noise".format(states, er, noise))

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
                    plt.savefig("../../results/graphs/pddm-network/{}/preference_trajectory_{}_agents_{}_states_{:.2f}_er_{:.2f}_noise{}.pdf".format(agent_type, agents, states, er, noise, closure))
                # Evidence-only graph
                elif conn == 0.0:
                    plt.savefig("../../results/graphs/pddm-network/{}/preference_trajectory_ev_only_{}_agents_{}_states_{:.2f}_er_{:.2f}_noise{}.pdf".format(agent_type, agents, states, er, noise, closure))
                plt.clf()