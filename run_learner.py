from world import World
import transforms
import pickle

# Start learning!

## Learn Q-table for the movement transform function.
#print "Learning Q-table for movement transform function..."
#position_transform_trainer = transforms.PositionTransformTrainer()
#ptt_policy = position_transform_trainer.learn_policy()
#pickle.dump(ptt_policy,open("resources/ptt_policy.pkl", "wb"))
#print ptt_policy
#
## Learn Q-table for mineral transform function.
#print "Learning Q-table for mineral transform function..."
#mineral_transform_trainer = transforms.MineralTransformTrainer()
#mtt_policy = mineral_transform_trainer.learn_policy()
#pickle.dump(mtt_policy,open("resources/mtt_policy.pkl", "wb"))
#print mtt_policy
#
## Learn Q-table for bamboo transform function.
#print "Learning Q-table for bamboo transform function..."
#bamboo_transform_trainer = transforms.BambooTransformTrainer()
#btt_policy = bamboo_transform_trainer.learn_policy()
#pickle.dump(btt_policy,open("resources/btt_policy.pkl", "wb"))
#print btt_policy
#
## Learn Q-table for arrow construction transform function.
#print "Learning Q-table for arrow construction transform function..."
#arrow_construction_transform_trainer = transforms.ArrowConstructionTransformTrainer()
#actt_policy = arrow_construction_transform_trainer.learn_policy()
#pickle.dump(actt_policy,open("resources/actt_policy.pkl", "wb"))
#print actt_policy

# Learn Q-table for full state space transform function.
print "Learning Q-table for full state space transform function..."
full_transform_trainer = transforms.FullTransformTrainer(2, 1)
ftt_policy = full_transform_trainer.learn_policy()
pickle.dump(ftt_policy,open("resources/ftt_policy.pkl", "wb"))
#print ftt_policy
print "Done!"