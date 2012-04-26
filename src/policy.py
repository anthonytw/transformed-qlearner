# Policy class.
class Policy:
    def __init__(self):
        self.action_map = None
        self.value_map = None
    
    # Get best action and reward at a given state.
    def item(self, state):
        action = self.action_map.item(tuple(state))
        value = self.value_map.item(tuple(state))
        return action, value
    
    # Representation.
    def __repr__(self):
        return "Action Map:\n" + self.action_map.__repr__() + "\nValue Map:\n" + self.value_map.__repr__()