import numpy
import random

class QLearner:
    # Initialize the state space Q-learner representation.
    def __init__(
        self,
        state_space,
        actions,
        action_callback,
        learning_rate = 0.1,
        discount_factor = 0.6):
        
        self.state_space = state_space
        self.actions = actions
        self.action_callback = action_callback
        
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        
        # Initialize state space dimensions.
        self.state_space_dim = []
        for elem in state_space:
            self.state_space_dim.append(len(elem))
            
        # Initialize action dimension.
        self.action_dim = len(actions)
        
        # Initialize SXA dimensions.
        self.state_space_action_dim = self.state_space_dim[:];
        self.state_space_action_dim.append(self.action_dim)
        
        # Initialize Q-table.
        self.q_table = numpy.zeros(self.state_space_action_dim)
        
        # Initialize R-table.
        self.r_table = numpy.zeros(self.state_space_dim)
    
    # Get a value in the R-table.
    def get_r_value(self, state):
        return self.r_table.item(tuple(state))
    
    # Set a value in the R-table.
    def set_r_value(self, state, value):
        self.r_table.itemset(state, value)
        
    # Get Q-value at a state X action.
    def get_q_value(self, state, action):
        sxa = state[:]
        sxa.append(action)
        return self.q_table.item(tuple(sxa))
        
    # Get the maximum Q-value at a state.
    def get_max_q_value(self, state):
        max_q_value = self.get_q_value(state, self.action_dim - 1)
        for action_index in xrange(self.action_dim-1):
            q_value = self.get_q_value(state, action_index)
            if q_value > max_q_value:
                max_q_value = q_value
        return max_q_value
    
    # Set Q value at a state X action.
    def set_q_value(self, state, action, value):
        sxa = state[:]
        sxa.append(action)
        self.q_table.itemset(tuple(sxa), value)
        
    # Select an action at random.
    def select_random_action(self):
        return random.randint(0, self.action_dim-1)
    
    # Select a random state.
    def select_random_state(self):
        random_state = []
        for state_elem_dim in self.state_space_dim:
            random_state.append(random.randint(0,state_elem_dim-1))
        return random_state
    
    # Execute state transition.
    def transition(self, state, action):
        # Execute action.
        next_state = self.action_callback(state, action)
        
        # Get reward value.
        reward = self.get_r_value(next_state)
        
        # Done.
        return next_state, reward
    
    # Execute a Q-learning episode.
    def execute_episode(self, initial_state, goal_state, max_actions):
        # Execute episode iterations.
        current_state = initial_state
        for iteration in xrange(max_actions):
            # At goal state?
            if tuple(current_state) == goal_state:
                break;
            
            # Execute random action.
            action = self.select_random_action()
            next_state, reward = self.transition(current_state, action)
            
            # Update Q-table.
            current_q_value = self.get_q_value(current_state, action)
            next_max_q_value = self.get_max_q_value(next_state)
            self.set_q_value(
                current_state,
                action,
                current_q_value \
                    + self.learning_rate \
                        * (reward \
                            + self.discount_factor * next_max_q_value
                            - current_q_value) )
            
            # Update state.
            current_state = next_state
            
    # Execute Q-learner.
    def execute(self, goal_state, episodes = 500, max_actions = 100):
        while episodes > 0:
            initial_state = self.select_random_state()
            self.execute_episode(initial_state, goal_state, max_actions)
            episodes -= 1