from world import World
import transforms
import cPickle

# Start learning!

# Learn Q-table for the movement transform function.
print "Learning Q-table for movement transform function..."
position_transform_trainer = transforms.PositionTransformTrainer()
ptt_policy = position_transform_trainer.learn_policy()
cPickle.dump(ptt_policy,open("resources/ptt_policy.pkl", "wb"))
print ptt_policy

# Learn Q-table for mineral transform function.
print "Learning Q-table for mineral transform function..."
mineral_transform_trainer = transforms.MineralTransformTrainer()
mtt_policy = mineral_transform_trainer.learn_policy()
cPickle.dump(mtt_policy,open("resources/mtt_policy.pkl", "wb"))
print mtt_policy

# Learn Q-table for bamboo transform function.
print "Learning Q-table for bamboo transform function..."
bamboo_transform_trainer = transforms.BambooTransformTrainer()
btt_policy = bamboo_transform_trainer.learn_policy()
cPickle.dump(btt_policy,open("resources/btt_policy.pkl", "wb"))
print btt_policy

# Learn Q-table for arrow construction transform function.
print "Learning Q-table for arrow construction transform function..."
arrow_construction_transform_trainer = transforms.ArrowConstructionTransformTrainer()
actt_policy = arrow_construction_transform_trainer.learn_policy()
cPickle.dump(actt_policy,open("resources/actt_policy.pkl", "wb"))
print actt_policy