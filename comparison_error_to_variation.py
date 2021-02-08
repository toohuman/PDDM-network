from utilities import preferences
import numpy as np

noise_params = [0.0, 1.0, 2.5, 5.0, 7.5, 10.0, 100.0]
noise_param = 0.0
comparison_errors = []
states = 10

rng = np.random.default_rng(128)
sample_size = 10000

quality_values = [round(i/(states + 1), 5) for i in range(1, states + 1)]
print("Quality values:", quality_values)

for noise_param in noise_params:
    comparison_errors[:] = []
    for state in range(1, states):
        comparison_errors.append(
            preferences.comparison_error(
                state / states,
                noise_param
            )
        )
    # print("Comparison errors:", comparison_errors)

    x = quality_values[0]
    y = quality_values[1]
    X = list()
    Y = list()

    x_greater_y = dict()

    # print(["{:.2f}".format(nv) for nv in np.linspace(0,1.0,100)])

    for noise_value in np.linspace(0,1.0,100):
        X.append([rng.normal(x, noise_value) for _ in range(sample_size)])
        Y.append([rng.normal(y, noise_value) for _ in range(sample_size)])

        x_greater_y["{:.2f}".format(noise_value)] = np.average(np.sum(X[-1] > Y[-1]))
        x_greater_y["{:.2f}".format(noise_value)] =\
            np.count_nonzero(
                np.greater(
                    X[-1], Y[-1]
                )
            )/sample_size

    ordered_keys = sorted(x_greater_y.keys())

    print("For lambda = ", noise_param, "with comparison error", comparison_errors[0],":")
    prev_key = None
    for k, key in enumerate(ordered_keys):
        if x_greater_y[key] >= comparison_errors[0]:
            print("Closest matching keys:", prev_key, ":", x_greater_y[prev_key], end=" | ")
            print(key, ":", x_greater_y[key], end=" | ")
            try:
                print(ordered_keys[k+1], ":", x_greater_y[ordered_keys[k+1]])
            except:
                pass
            break
        else:
            prev_key = key
