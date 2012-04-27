from positiontransform import *
from mineraltransform import *
from bambootransform import *
from arrowconstructiontransform import *
from fulltransform import *

from world import World

class TransformSet:
    def __init__(self, q_table_directory, world, full_transform):
        # Load transform functions and weights.
        self.transforms = []
        if full_transform:
            self.transforms.append([1.0, FullTransform.from_file(q_table_directory + "/ftt_policy.pkl", world.cell_width, world.cell_height)])
        else:
            self.transforms.append([1.0, PositionTransform.from_file(q_table_directory + "/ptt_policy.pkl")])
            self.transforms.append([1.0, MineralTransform.from_file(q_table_directory + "/mtt_policy.pkl")])
            self.transforms.append([1.0, BambooTransform.from_file(q_table_directory + "/btt_policy.pkl")])
            self.transforms.append([1.0, ArrowConstructionTransform.from_file(q_table_directory + "/actt_policy.pkl")])
    
    # Determine the best action to perform given the transform functions and the
    # current state.
    def get_best_action(self, state):
        best_action = World.Action.Move_Down
        best_action_q_value = 0
        for transform in self.transforms:
            action, q_value = transform[1].get_best_action(state)
            q_value *= transform[0]
            
            print " - [%2d] %s -> %s" % (q_value, transform[1].__class__.__name__, World.Action.name[action])
            
            if q_value > best_action_q_value:
                best_action_q_value = q_value
                best_action = action
            
        # If best action Q-value is zero, there is no good action. Do nothing!    
        if best_action_q_value == 0:
            best_action = World.Action.Do_Nothing
            
        return best_action, best_action_q_value