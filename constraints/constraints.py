import numpy as np

# because the descriptions are saved in a dictionary
# it is possible to compare them without reordering them
# the binary, nominal (tuple), ordinal (Index) and numerical (tuple) can be handled
def check_similar_description(desc=None, cq_satisfied=None):

    constraint_similar_description = False

    # check for redundant descriptions (the exact same description but in another order)
    # the comparison has to be done with the candidate queue of the current iteration only
    # this queue is saved in cq_satisfied
    # in theory, a refinement at the current level can be similar to a desc from an earlier level
    # this can happen for numerical and ordinal attributes
    # chances are low that those descriptions will end up in the result list together
    for seed in cq_satisfied:

        current = desc['description'].copy()
        new = seed['description'].copy()
        if current == new: # we have to apply a constraint
            constraint_similar_description = True
            break

    return constraint_similar_description

# the min_size values are saved in general_params
def check_subgroup_size(idxIDs=None, general_params=None, alg_constraints=None):

    constraint_subgroup_size = False

    # if subgroup is too small, we have to apply a constraint
    if len(idxIDs['idx_id']) < alg_constraints['min_size']*len(general_params['IDs']):
        constraint_subgroup_size = True

    return constraint_subgroup_size

