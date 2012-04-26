from world import World
from qlearner import QLearner
import cPickle

# Bamboo transformation.
class ArrowConstructionTransform:
    def __init__(self):
        # Define state space.
        # ss = [ enough_resources, arrow_construction_state ]
        self.state_space = []
        self.state_space.append([ \
            False,
            True
            ])
        self.state_space.append([ \
            World.ArrowState.Not_Started,
            World.ArrowState.Tips_Formed,
            World.ArrowState.Fins_Formed,
            World.ArrowState.Shafts_Formed,
            World.ArrowState.Arrows_Complete ])
        self.state_space_dim = []
        for state_values in self.state_space:
            self.state_space_dim.append(len(state_values))
        
        # Define action set.
        self.actions = [ \
            World.Action.Form_Tips,
            World.Action.Form_Fins,
            World.Action.Form_Shafts,
            World.Action.Connect_Parts ]
        
        # Define empty policy.
        self.policy = None
    
    @classmethod
    def from_file(cls, filename):
        transform = cls()
        transform.policy = cPickle.load(open(filename, "rb"))
        return transform
    
    # Pull a policy action if the policy is set.
    def get_best_action(self, state):
        if self.policy == None:
            return World.Action.Move_Down, 0
        return self.policy.item(state)
        
    # Use the transformation to reduce a state.
    def reduce_state(self, state):
        # Enough resources?
        enough_resources = \
            (state.minerals >= state._world.needed_minerals) \
            and (state.bamboo >= state._world.needed_bamboo)
        enough_resources_index = self.state_space[0].index(enough_resources)
            
        # Get arrow state index.
        arrow_state = state.arrows
        if arrow_state not in self.state_space[1]:
            print "AS %d not in %s" % (arrow_state, str(self.state_space[1]))
            arrow_state = self.state_space[1][0]
        arrow_state_index = self.state_space[1].index(arrow_state)
        
        # Return reduced state.
        return [enough_resources_index, arrow_state_index]

# Bamboo transformation Q-learning trainer.
class ArrowConstructionTransformTrainer(ArrowConstructionTransform):
    def __init__(self):
        # Initialize super.
        ArrowConstructionTransform.__init__(self)
        
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
        goal_states = [ \
            ( 0, self.state_space[1].index(World.ArrowState.Arrows_Complete) ),
            ( 1, self.state_space[1].index(World.ArrowState.Arrows_Complete) ) ]
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
        expanded_state.arrows = self.state_space[1][reduced_state[1]]
        expanded_state.minerals = expanded_state._world.needed_minerals if self.state_space[0][reduced_state[0]] else 0
        expanded_state.bamboo = expanded_state._world.needed_bamboo if self.state_space[0][reduced_state[0]] else 0
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        