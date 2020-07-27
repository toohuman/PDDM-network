import os
import sys

states_set = [10, 20]
agents_set = [100]
evidence_rates = [0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
noise_levels = [0, 1, 10, 100]
connectivity_values = [0.0, 0.01, 0.02, 0.05, 0.1, 0.5, 1.0]

directory = "../results/test_results/pddm-network/"

files = os.listdir(directory)

# Rename files based on parameter naming schemes.

# for file in files:
#     print(file, "====> ",end="")
#     file_name = file.split('_')
#     # print(file_name)

#     file_name_parts = []
#     offset = 0
#     if file_name[0] == 'loss':
#         file_name_parts.append("loss")
#     else:
#         file_name_parts.append("steady_state_loss")
#         offset = 2
#     file_name_parts += [
#         "{}a".format(file_name[1 + offset]),
#         "{}s".format(file_name[3 + offset]),
#         "{:.2f}con".format(float(file_name[5 + offset])),
#         "{:.2f}er".format(float(file_name[7 + offset])),
#         "{}nv".format(file_name[9 + offset].split('.')[0]),
#         "{}_{}".format(file_name[11 + offset], file_name[12 + offset])
#     ]
#     # print("_".join(file_name_parts))
#     file_name = "_".join(map(lambda x: str(x), file_name_parts))
#     print(file_name)
    # os.rename(directory + file, directory + file_name)

# Rename loss files to error files.
for file in files:
    print(file, "====> ",end="")
    file_name = file.split('_')
    print(file_name)

    try:
        loss = file_name.index('loss')
    except ValueError:
        continue
    file_name[loss] = "error"

    file_name = "_".join(map(lambda x: str(x), file_name))
    print(file_name)
    os.rename(directory + file, directory + file_name)

