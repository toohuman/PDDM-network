import math
import random


def ignorant_preferences(states):
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
        return round(bound * (1 - x), 5)

    error_value = ( pow(math.e, -param * x) - pow(math.e, -param) )\
                / ( 1.0 - pow(math.e, -param) )

    return round(bound * error_value, 5)

