from world import World
from qlearner import QLearner
import pickle

# Mineral transformation.
class MineralTransform:
    def __init__(self):
        # Define state space.
        self.state_space = []
        self.state_space.append([ \
            World.SiteState.Useless,
            World.SiteState.Mineral_Deposit,
            World.SiteState.Minerals_Exposed,
            World.SiteState.Minerals_Separated ])
        self.state_space_dim = [len(self.state_space[0])]
        
        # Define action set.
        self.actions = [ \
            World.Action.Dig,
            World.Action.Separate,
            World.Action.Extract ]
        
        # Define empty policy.
        self.policy = None
    
    @classmethod
    def from_file(cls, filename):
        transform = cls()
        transform.policy = pickle.load(open(filename, "rb"))
        return transform
    
    # Pull a policy action if the policy is set.
    def get_best_action(self, state):
        if self.policy == None:
            return World.Action.Move_Down, 0
        return self.policy.item(self.reduce_state(state))
        
    # Use the transformation to reduce a state.
    def reduce_state(self, state):
        # Get site state.
        site_state = state.site_state()
        
        # In the useful states?
        if site_state not in self.state_space[0]:
            site_state = World.SiteState.Useless
        
        # Get index.
        site_state = self.state_space[0].index(site_state)
        
        # Return reduced state.
        return [site_state]

# Mineral transformation Q-learning trainer.
class MineralTransformTrainer(MineralTransform):
    def __init__(self):
        # Initialize super.
        MineralTransform.__init__(self)
        
        # Define training world.
        self.training_world = World(1, 1)
        self.reset_training_world()
    
    # Learn the Q-table.
    def learn_policy(self):
        # Initialize Q-learner.
        qlearner = QLearner( \
            self.state_space,
            self.actions,
            self.handle_action,
            self.reset_training_world )
        
        # Initialize reward states.
        goal_states = [( self.state_space[0].index(World.SiteState.Useless), )]
        for goal_state in goal_states:
            qlearner.set_r_value( goal_state, 100 )
        
        #print qlearner.r_table
        
        # Run Q-learner.
        qlearner.execute(goal_states, 300, 30)
        
        # Return policy.
        return qlearner.get_policy()
    
    # Expands the reduced state into the training world.
    def expand_training_state(self, reduced_state):
        # Set world state based on reduced state.
        expanded_state = World.State.from_state(self.training_world.agent_state)
        self.training_world.world_state[0][0] = self.state_space[0][reduced_state[0]]
        return expanded_state
    
    # Resets the training world.
    def reset_training_world(self):
        self.training_world.world_state[0][0] = World.SiteState.Useless
    
    # Handles an action.
    def handle_action(self, reduced_state, action_index):
        action = self.actions[action_index]
        expanded_state = self.expand_training_state(reduced_state)
        #print " -- Reduced state : " + str(reduced_state)
        #print " -- Expanded state: " + str(expanded_state)
        expanded_state = self.training_world.perform_action(expanded_state, action)
        #print " -- Expanded state: " + str(expanded_state)
        new_reduced_state = self.reduce_state(expanded_state)
        #print " -- Reduced state : " + str(new_reduced_state)
                
        return new_reduced_state