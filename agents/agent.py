from utilities import operators

class Agent:

    preferences     = None
    evidence        = int
    interactions    = int
    since_change    = int
    form_closure = bool

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

