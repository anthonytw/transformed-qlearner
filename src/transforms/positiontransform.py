from world import World
from qlearner import QLearner
import pickle

# Position transformation.
class PositionTransform:
    class HorizontalState:
        Left_Of = -1
        At = 0
        Right_Of = 1
        
    class VerticleState:
        Above = -1
        At = 0
        Below = 1
        
    def __init__(self):
        # Define state space.
        self.state_space = []
        self.state_space.append([ \
            PositionTransform.HorizontalState.Left_Of,
            PositionTransform.HorizontalState.At,
            PositionTransform.HorizontalState.Right_Of ])
        self.state_space.append([ \
            PositionTransform.VerticleState.Above,
            PositionTransform.VerticleState.At,
            PositionTransform.VerticleState.Below ])
        
        # Define action set.
        self.actions = [ \
            World.Action.Move_Down,
            World.Action.Move_Left,
            World.Action.Move_Right,
            World.Action.Move_Up ]
        
        # Define empty policy.
        self.policy = None
    
    @classmethod
    def from_file(cls, filename):
        transform_function = cls()
        transform_function.policy = pickle.load(open(filename, "rb"))
        return transform_function
    
    # Pull a policy action if the policy is set.
    def get_best_action(self, state):
        if self.policy == None:
            return World.Action.Move_Down, 0
        return self.policy.item(self.reduce_state(state))
        
    # Use the transformation to reduce a state.
    def reduce_state(self, state):
        world = state._world
        
        # Find closest useful resource.
        useful_site_states = []
        if state.minerals < world.needed_minerals:
            useful_site_states += [ \
                World.SiteState.Mineral_Deposit,
                World.SiteState.Minerals_Exposed,
                World.SiteState.Minerals_Separated ]
        if state.bamboo < world.needed_bamboo:
            useful_site_states += [ \
                World.SiteState.Good_Soil,
                World.SiteState.Tilled,
                World.SiteState.Bamboo_Sprouted ]
            
        closest_x_offset = 0
        closest_y_offset = 0
        closest_offset   = world.cell_height*world.cell_width
        for y in xrange(world.cell_height):
            for x in xrange(world.cell_width):
                if world.world_state[y][x] in useful_site_states:
                    x_offset = state.x - x
                    y_offset = state.y - y
                    offset = abs(y_offset) + abs(x_offset)
                    if offset < closest_offset:
                        closest_x_offset = x_offset
                        closest_y_offset = y_offset
                        closest_offset = offset
                                    
        # Determine offset states.
        horizontal_state = 1 if closest_x_offset == 0 else closest_x_offset / abs(closest_x_offset) + 1
        vertical_state = 1 if closest_y_offset == 0 else closest_y_offset / abs(closest_y_offset) + 1
        
        # Return reduced state.
        return [horizontal_state, vertical_state]

# Position transformation Q-learning trainer.
class PositionTransformTrainer(PositionTransform):
    def __init__(self):
        # Initialize super.
        PositionTransform.__init__(self)
        
        # Define training world.
        self.training_world = World(3, 3)
        self.training_world.world_state \
            [PositionTransform.VerticleState.At + 1] \
            [PositionTransform.HorizontalState.At + 1] = World.SiteState.Mineral_Deposit
    
    # Learn the Q-table.
    def learn_policy(self):
        # Initialize Q-learner.
        qlearner = QLearner( \
            self.state_space,
            self.actions,
            self.handle_action,
            self.reset_training_world )
        
        # Initialize reward states.
        goal_states = [( \
            PositionTransform.HorizontalState.At + 1,
            PositionTransform.VerticleState.At + 1 )]
        for goal_state in goal_states:
            qlearner.set_r_value( goal_state, 100 )
        
        #print qlearner.r_table
        
        # Run Q-learner.
        qlearner.execute(goal_states, 500, 100)
        
        # Return policy.
        return qlearner.get_policy()
    
    # Expands the reduced state into the training world.
    def expand_training_state(self, reduced_state):
        # Set world state based on reduced state.
        expanded_state = World.State.from_state(self.training_world.agent_state)
        expanded_state.x = reduced_state[0]
        expanded_state.y = reduced_state[1]
        return expanded_state
    
    # Resets the training world.
    def reset_training_world(self):
        # Training world does not require a reset in this transformation.
        pass
    
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
