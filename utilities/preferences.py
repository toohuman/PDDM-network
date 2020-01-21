import math
import random

def ignorant_pref_generator(states):
    """ Returns an empty set of preferences to denote complete uncertainty. """

    return set()

def comparison_error(x: float, param: float):
    """
    Generate the error function for calculating probabilities of confusing
    one option for an alternative, depending on their relative placement
    to one another.
    """

    # Bound the error function in [0, bound]
    bound = 0.5

    # Special case:
    if param == 0.0:
        return 0.0

    error_value = ( pow(math.e, -param * x) - pow(math.e, -param) )\
                / ( 1.0 - pow(math.e, -param) )

    return round(bound * error_value, 5)


def random_evidence(states, true_order, noise_value, comparison_errors, random_instance):
    """ Generate a random piece of evidence. """

    evidence = set()
    shuffled_states = [x for x in range(states)]
    random_instance.shuffle(shuffled_states)
    index_i = shuffled_states.pop()
    index_j = shuffled_states.pop()

    pos_i = true_order.index(index_i)
    pos_j = true_order.index(index_j)

    if pos_i < pos_j:
        best_index = index_i
        worst_index = index_j
    else:
        best_index = index_j
        worst_index = index_i

    if noise_value is None:
        evidence.add((best_index, worst_index))
        return evidence

    difference = abs(pos_i - pos_j) - 1
    comp_error = comparison_errors[difference]

    if random_instance.random() > comp_error:
        evidence.add((best_index, worst_index))
    else:
        evidence.add((worst_index, best_index))

    return evidence