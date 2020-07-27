# This file contains the functions for calculating results from the agents'
# preferences, as well as writing the results to a file.


def error(preferences, true_preferences, normalised = True):
    """
    Inspired by a loss function in machine learning, this function calculates
    the sum of the differences of two matrices, scaled by 0.5 so that we count
    half-values for having no preference between two elements.
    The idea is that we compare the agent's preferences with the true state of
    the world and a return value of 0 indicates no differences (100% similarity)
    or "zero loss" between the true value and the agents' preferences.

    The normalisation option uses the worst possible preference (in relation to
    the true state of the world) to normalise the values in [0, 1].
    """

    # Sum all of the inconsistent pairs of preference relations as 1s.
    differences = sum(1 for (x,y) in preferences if (y,x) in true_preferences)

    # Sum all of the missing pairs of preference relations as 1/2s.
    differences += 0.5 * (abs(len(true_preferences) - len(preferences)))

    # If normalising the result (default) then divide the sum of the differences
    # by the length of the maximum number of pairs of relations.
    if normalised:
        return differences / len(true_preferences)

    return differences


def uncertainty(preferences, true_preferences, normalised = True):
    """
    Calculate the number if "missing" or "absent" preference pairs in an agent's
    belief compared to the number in the true preference ordering, as this will
    identify how "uncertaint" the agent is.

    Normalised, this provides us with an uncertainty metric in [0, 1] where
    ignorant agents start out completely uncertain and decrease their uncertainty
    over time.
    """

    # Sum the total of missing pairs of preference relations.
    differences = abs(len(true_preferences) - len(preferences))

    # If normalising the result (default) then divide the sum of the differences
    # by the length of the maximum number of pairs of relations.
    if normalised:
        return differences / len(true_preferences)

    return differences


def expected_error(noise_param, states):
    """
    The expected error of the system given noise_param lambda and the number
    of states. With the number of states we can identify the total number of
    comparisons nC2. Then, we can identify the number of comparisons of
    distance 1 = n-1, 2 = n-2, ..., n-1 = 1. The expected error is then given
    by the sum of multiplying each comparison error by the probability of that
    comparison occurring.
    """

    from math import comb
    import preferences

    comparison_errors = [
        preferences.comparison_error(
            state / states,
            noise_param
        )
        for state in range(1, states)
    ]

    n_choose_2 = comb(states, 2)

    expected_error = 0.0
    for i, p in enumerate([(states - x)/n_choose_2 for x in range(1, states)]):
        expected_error += p * comparison_errors[i]

    return round(expected_error, 3)


def write_to_file(directory, file_name, params, data, max, array_data = False):
    """
    Write the results arrays to a file. The array_data argument allows us to write
    nested (array) data for recording the agents' averaged preferences for each state
    while reusing the same function for writing single value averages, e.g., loss.
    """

    with open(directory + file_name + '_' + '_'.join(params) + '.csv', 'w') as file:
        for i, test_data in enumerate(data):
            for j, results_data in enumerate(test_data):
                if array_data:
                    file.write('[')
                    for k, sub_data in enumerate(results_data):
                        file.write('{:.4f}'.format(sub_data))
                        if k != len(results_data) - 1:
                            file.write(',')
                    file.write(']')
                else:
                    file.write('{:.4f}'.format(results_data))
                # Determine whether the line ends here
                if j != len(test_data) - 1:
                    file.write(',')
                else:
                    file.write('\n')
            if i > max:
                break


if __name__ == '__main__':

    noise_param = 0
    print("Expected error for {} states and lambda = {}: {}".format(x := 5, noise_param, expected_error(0, x)))
    print("Expected error for {} states and lambda = {}: {}".format(x := 10, noise_param, expected_error(0, x)))
    print("Expected error for {} states and lambda = {}: {}".format(x := 20, noise_param, expected_error(0, x)))
