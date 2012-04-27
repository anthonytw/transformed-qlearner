from world import World
from qlearner import QLearner
import numpy
import pickle

# Full transformation.
class FullTransform:
    class StateOffset:
        World       = 0
        X           = 0
        Y           = 1
        Minerals    = 2
        Bamboo      = 3
        Arrows      = 4
        
    def __init__(self, cell_width, cell_height):
        # Enumerate states.
        enum_site_state = [ \
            World.SiteState.Useless,
            World.SiteState.Mineral_Deposit,
            World.SiteState.Minerals_Exposed,
            World.SiteState.Minerals_Separated,
            World.SiteState.Good_Soil,
            World.SiteState.Tilled,
            World.SiteState.Bamboo_Planted,
            World.SiteState.Bamboo_Sprouted ]
        
        self.world_shape = (cell_width, cell_height)
        self.world_size = cell_width * cell_height
        
        # Define state space.
        # ss = { w_0,0, ... w_w,h, x, y, minerals, bamboo, arrows }
        self.state_space = []
        for y in xrange(cell_height):
            for x in range(cell_width):
                self.state_space.append(enum_site_state[:])
        offset = len(self.state_space)
        self.state_space.append(range(0,cell_width))
        self.state_space.append(range(0,cell_height))
        self.state_space.append(range(0,151,50))
        self.state_space.append(range(0,151,50))
        self.state_space.append([ \
            World.ArrowState.Not_Started,
            World.ArrowState.Tips_Formed,
            World.ArrowState.Fins_Formed,
            World.ArrowState.Shafts_Formed,
            World.ArrowState.Arrows_Complete ])
        self.state_space_dim = []
        for state_enum in self.state_space:
            self.state_space_dim.append(len(state_enum))
            
        FullTransform.StateOffset.X += offset
        FullTransform.StateOffset.Y += offset
        FullTransform.StateOffset.Minerals += offset
        FullTransform.StateOffset.Bamboo += offset
        FullTransform.StateOffset.Arrows += offset
        
        # Define action set.
        self.actions = [ \
            World.Action.Move_Down,
            World.Action.Move_Left,
            World.Action.Move_Right,
            World.Action.Move_Up,
            World.Action.Dig,
            World.Action.Separate,
            World.Action.Extract,
            World.Action.Till,
            World.Action.Plant,
            World.Action.Harvest,
            World.Action.Form_Tips,
            World.Action.Form_Fins,
            World.Action.Form_Shafts,
            World.Action.Connect_Parts,
            World.Action.Do_Nothing ]
        self.action_dim = len(self.actions)
        
        # Define empty policy.
        self.policy = None
    
    @classmethod
    def from_file(cls, filename, cell_width, cell_height):
        transform = cls(cell_width, cell_height)
        transform.policy = pickle.load(open(filename, "rb"))
        return transform
    
    # Pull a policy action if the policy is set.
    def get_best_action(self, state):
        if self.policy == None:
            return World.Action.Do_Nothing, 0
        return self.policy.item(self.reduce_state(state))
        
    # Use the transformation to reduce a state.
    def reduce_state(self, state):
        reduced_state = []
        
        # Get world.
        world = state._world
        
        # Get site states.
        # NOTE: Normally the indices should be used, but in this case indices
        # are the same as the values.
        for y in xrange(self.world_shape[1]):
            for x in xrange(self.world_shape[0]):
                reduced_state.append(world.world_state[y][x])
        
        reduced_state.append(state.x)
        reduced_state.append(state.y)
        
        # Limit minerals.
        if state.minerals in self.state_space[FullTransform.StateOffset.Minerals]:
            reduced_state.append(self.state_space[FullTransform.StateOffset.Minerals].index(state.minerals))
        elif state.minerals > 150:
            reduced_state.append(self.state_space_dim[FullTransform.StateOffset.Minerals] - 1)
        else:
            reduced_state.append(0)
            
        # Limit bamboo.
        if state.bamboo in self.state_space[FullTransform.StateOffset.Bamboo]:
            reduced_state.append(self.state_space[FullTransform.StateOffset.Bamboo].index(state.bamboo))
        elif state.bamboo > 150:
            reduced_state.append(self.state_space_dim[FullTransform.StateOffset.Bamboo] - 1)
        else:
            reduced_state.append(0)
            
        reduced_state.append(state.arrows)
        
        # Return reduced state.
        return reduced_state

# Full transformation Q-learning trainer.
class FullTransformTrainer(FullTransform):
    def __init__(self, cell_width, cell_height):
        # Initialize super.
        FullTransform.__init__(self, cell_width, cell_height)
        
        # Define training world.
        self.training_world = World(cell_width, cell_height)
        self.reset_training_world()
    
    # Learn the Q-table.
    def learn_policy(self):
        # Initialize Q-learner.
        qlearner = QLearner( \
            self.state_space,
            self.actions,
            self.handle_action,
            self.reset_training_world )
        
        # Initialize goal states.
        goal_states = []
        print "Enumerating goal states..."
        for state_index in xrange(qlearner.r_table.size):
            state = numpy.unravel_index(state_index, qlearner.r_table.shape)
            if state[FullTransform.StateOffset.Arrows] == World.ArrowState.Arrows_Complete:
                goal_states.append(tuple(state))
        print "Goal states: %d" % len(goal_states)
        
        for goal_state in goal_states:
            qlearner.set_r_value( goal_state, 100 )
        
        #print qlearner.r_table
        
        # Run Q-learner.
        qlearner.execute(goal_states, 20000, 15)
        
        # Return policy.
        return qlearner.get_policy()
    
    # Expands the reduced state into the training world.
    def expand_training_state(self, reduced_state):
        # Set world state based on reduced state.
        expanded_state = World.State.from_state(self.training_world.agent_state)
        world = expanded_state._world
        
        # Set world state.
        for index in xrange(self.world_size):
            (x, y) = numpy.unravel_index(index, self.world_shape)
            world.world_state[y][x]
        
        # Set other elements.
        expanded_state.x = reduced_state[FullTransform.StateOffset.X]
        expanded_state.y = reduced_state[FullTransform.StateOffset.Y]
        expanded_state.minerals = 50 * reduced_state[FullTransform.StateOffset.Minerals]
        expanded_state.bamboo = 50 * reduced_state[FullTransform.StateOffset.Bamboo]
        expanded_state.arrows = reduced_state[FullTransform.StateOffset.Arrows]
            
        return expanded_state
    
    # Resets the training world.
    def reset_training_world(self):
        pass
        
    # Handles an action.
    def handle_action(self, reduced_state, action_index):
        action = self.actions[action_index]
        expanded_state = self.expand_training_state(reduced_state)
        expanded_state = self.training_world.perform_action(expanded_state, action)
        new_reduced_state = self.reduce_state(expanded_state)
                
        return new_reduced_state