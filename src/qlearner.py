import numpy
import random
from policy import *
import time

class QLearner:
    # Initialize the state space Q-learner representation.
    def __init__(
        self,
        state_space,
        actions,
        action_callback,
        reset_callback,
        learning_rate = 0.1,
        discount_factor = 0.6):
        
        self.state_space = state_space
        self.actions = actions
        self.action_callback = action_callback
        self.reset_callback = reset_callback
        
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
        self.r_table.itemset(tuple(state), value)
        
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
        
    # Return the policy with best values chosen at each state.
    def get_policy(self):
        policy = Policy()
        policy.value_map  = numpy.zeros(self.state_space_dim)
        policy.action_map = numpy.zeros(self.state_space_dim, numpy.int)
        
        for state_index in xrange(policy.action_map.size):
            state = list(numpy.unravel_index(state_index, policy.action_map.shape))
            
            # Find best action and associated Q-value.
            best_action_index = 0
            best_action_value = 0
            for action_index in xrange(self.action_dim):
                q_value = self.get_q_value(state, action_index)
                if q_value > best_action_value:
                    best_action_value = q_value
                    best_action_index = action_index
            
            # Set action and value in map.
            policy.value_map.itemset(tuple(state), best_action_value)
            policy.action_map.itemset(tuple(state), self.actions[best_action_index])
        
        # Done.
        return policy
        
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
    def execute_episode(self, initial_state, goal_states, max_actions):
        # Execute episode iterations.
        current_state = initial_state
        for iteration in xrange(max_actions):
            # At goal state?
            if tuple(current_state) in goal_states:
                break;
            
            # Execute random action.
            action = self.select_random_action()
            next_state, reward = self.transition(current_state, action)
            
            #print str(current_state) + " + A:[i" + str(action) + "|" + str(self.actions[action]) + "] --> " + str(next_state) + " R:" + str(reward)
            
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
            
        return iteration + 1
            
    # Execute Q-learner.
    def execute(self, goal_state, episodes = 100, max_actions = 20):
        scale = 100.0 / episodes
        on_episode = 0
        average_iterations = 0.0
        max_iterations = 0
        start_time_t = time.time()
        start_time = time.clock()
        while episodes > 0:
            self.reset_callback()
            initial_state = self.select_random_state()
            
            # Output status.
            iterations = self.execute_episode(initial_state, goal_state, max_actions)
            if iterations > max_iterations:
                max_iterations = iterations
            average_iterations = 0.5*(average_iterations + iterations)
            
            on_episode += 1
            if (on_episode % 100) == 1:
                # Calculate r_table sparseness.
                nonzero_values = 0
                for index in xrange(self.q_table.size):
                    if self.q_table.item(index) != 0:
                        nonzero_values += 1
                print "Q-table occupancy: %.2f%%" % (nonzero_values * 100.0 / self.q_table.size)
            if (on_episode % 50) == 1:
                print "[%4d of %4d (%6.2f%%)] Iterations: %d; Average: %.2f; Max: %d" % \
                    (on_episode, episodes, on_episode*scale, iterations, average_iterations, max_iterations)
                # Reset max...
                max_iterations = 0
            
            episodes -= 1
        end_time = time.clock()
        end_time_t = time.time()
        print "Elapsed wall time: %.4fms" % ((end_time_t-start_time_t)*1000.0)
        print "Total learning time: %.2fms" % ((end_time-start_time)*1000.0)