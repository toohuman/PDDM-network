from utilities import operators

class Agent:

    preferences     = None
    evidence        = int
    interactions    = int
    since_change    = int
    form_closure    = bool

    def __init__(self, preferences, form_closure):

        self.preferences = preferences
        self.evidence = 0
        self.interactions = 0
        self.since_change = 0
        self.form_closure = form_closure


    def steady_state(self, threshold):
        """ Check if agent has reached a steady state. """

        return True if self.since_change >= threshold else False


    def evidential_updating(self, preferences):
        """
        Update the agent's preferences based on the evidence they received.
        Increment the evidence counter.
        """

        # Form the transitive closure of the combined preference
        # prior to updating.
        if self.form_closure:
            operators.transitive_closure(preferences)

        # Track the number of iterations.
        if preferences == self.preferences:
            self.since_change += 1
        else:
            self.since_change = 0

        self.preferences = preferences
        self.evidence += 1


    def update_preferences(self, preferences):
        """
        Update the agent's preferences based on having combined their preferences with
        those of another agent.
        Increment the interaction counter.
        """

        # Form the transitive closure of the combined preference
        # prior to updating.
        if self.form_closure:
            operators.transitive_closure(preferences)

        # Track the number of iterations.
        if preferences == self.preferences:
            self.since_change += 1
        else:
            self.since_change = 0

        self.preferences = preferences
        self.interactions += 1


    def find_evidence(states, full_true_ordering, noise_value, comparison_errors, random_instance):
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

