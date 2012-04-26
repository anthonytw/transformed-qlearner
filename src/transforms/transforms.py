from positiontransform import *
from mineraltransform import *
from bambootransform import *
from arrowconstructiontransform import *

class TransformSet:
    def __init__(self, q_table_directory):
        # Load transform functinos and weights.
        self.transforms = []
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
            
            if q_value > best_action_q_value:
                best_action_q_value = q_value
                best_action = action
        return best_action, best_action_q_value