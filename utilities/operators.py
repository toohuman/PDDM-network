def combine(prefs1, prefs2):
    """
    A renormalised sum of the two preference sets.
    """

    # Combine the preference sets
    preferences = prefs1 | prefs2

    # Now remove inconsistencies
    consistent_prefs = [(x,y) for x,y in preferences if (y,x) not in preferences]
    preferences = set(consistent_prefs)

    return preferences


def transitive_closure(closure):
    """
    Form the transitive closure of the input set by filling in relations
    wherever they might be missing.
    """

    # Identify the transitive relations
    # Source: https://stackoverflow.com/questions/8673482/transitive-closure-python-tuples
    while True:
        new_relations = set((x,w) for x,y in closure for q,w in closure if q == y)
        # Form the union of the new relations with the current closure
        closure_until_now = closure | new_relations

        if closure_until_now == closure:
            break

        closure = closure_until_now

    # Return the complete preference ordering closed under transitivity.
    return closure
