from utilities import operators

import numpy as np

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


    @staticmethod
    def combine(prefs1, prefs2, form_closure):
        """
        A renormalised sum of the two preference sets.
        """

        # Combine the preference sets
        preferences = prefs1 | prefs2

        # Now remove inconsistencies
        consistent_prefs = [(x,y) for x,y in preferences if (y,x) not in preferences]
        preferences = set(consistent_prefs)

        if form_closure:
            preferences = transitive_closure(preferences)

        return preferences


    def evidential_updating(self, preferences):
        """
        Update the agent's preferences based on the evidence they received.
        Increment the evidence counter.
        """

        # Form the transitive closure of the combined preference
        # prior to updating.
        # if self.form_closure:
        #     operators.transitive_closure(preferences)

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
        # if self.form_closure:
        #     operators.transitive_closure(preferences)

        # Track the number of iterations.
        if preferences == self.preferences:
            self.since_change += 1
        else:
            self.since_change = 0

        self.preferences = preferences
        self.interactions += 1


    def find_evidence(self, states, true_prefs, noise_value, comparison_errors, random_instance):
        """ Generate a random piece of evidence from the set of unknown preference relations. """

        evidence = set()

        expanded_preferences = self.preferences | {(y,x) for x, y in self.preferences}
        possible_evidence = true_prefs.difference(expanded_preferences)
        # print(possible_evidence)

        try:
            choice = random_instance.sample(possible_evidence, 1)[0]
            # print(choice)
        except ValueError:
            return evidence

        if noise_value is None:
            evidence.add(choice)
            return evidence

        difference = abs(choice[0] - choice[1]) - 1
        comp_error = comparison_errors[difference]

        if random_instance.random() > comp_error:
            evidence.add(choice)
        else:
            evidence.add((choice[1], choice[0]))

        return evidence


    def random_evidence(self, states, true_order, noise_value, comparison_errors, random_instance):
        """ Generate a random piece of evidence regardless of current belief. """

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


class Probabilistic(Agent):

    """
    A probabilistic agent represents its belief by a probability distribution over the set of states.
    By updating their beliefs according to the updating/fusion rules implemented below, a preference
    ordering should be obtainable from their belief.
    """

    def __init__(self, belief):
        super().__init__(belief)
        # Alongside initialising an uncertain preference set, a probabilistic agent
        # also needs an uncertain probability distribution over the set of states.
        self.belief = np.full(states, 1/states)


    @staticmethod
    def consensus(belief1, belief2):
        """
        Probabilistic updating using the product operator. This combines two (possibly conflicting)
        probability distributions into a single probability distribution.
        """

        # Using the product operator defined in (Lee at al. 2018) and detailed further in (Lawry et al. 2019).
        # When compared with a possibilistic approach, this operator can be adjusted to produce probabilistic
        # rankings of states.
        product_sum = np.dot(belief1, belief2)
        new_belief = np.array([
            (belief1[i] * belief2[i]) /
            product_sum
            for i in range(len(belief1))
        ])

        invalid_belief = np.isnan(np.sum(new_belief))

        if not invalid_belief:
            return new_belief
        else:
            return None


    def evidential_updating(self, true_state, noise_value, random_instance):
        """
        Update the agent's belief based on the evidence they received.
        Increment the evidence counter.
        """

        evidence = self.random_evidence(
            true_state,
            noise_value,
            random_instance
        )

        new_belief = self.belief
        if evidence is not None:
            new_belief[evidence[0]] = evidence[1]

        # Track the number of iterations that the agent's belief has
        # remained unchanged.
        if np.array_equal(self.belief, new_belief):
            self.since_change += 1
        else:
            self.since_change = 0

        self.belief = new_belief
        self.evidence += 1


    def random_evidence(self, states, true_order, noise_value, comparison_errors, random_instance):
        """ Generate a random piece of evidence regardless of current belief. """

        evidence = np.full(states, 1/states)
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
            evidence[best_index] = (1 - qualities[best_index])/states
            for i, ev in evidence:
                if i != best_index:
                    evidence[i] = ((states - 1) *(qualities[best_index]) + 1)/states

            return evidence

        # To-do: Finish noisy evidence
        difference = abs(pos_i - pos_j) - 1
        comp_error = comparison_errors[difference]

        if random_instance.random() > comp_error:
            evidence.add((best_index, worst_index))
        else:
            evidence.add((worst_index, best_index))

        return evidence