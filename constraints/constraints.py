import numpy as np

# because the descriptions are saved in a dictionary
# it is possible to compare them without reordering them
# the binary, nominal (tuple), ordinal (list) and numerical (tuple) can be handled


def check_similar_description(desc=None, cq_satisfied=None, d_i=None, current_beam=None):

    constraint_similar_description = False

    # check for redundant descriptions (the exact same description but in another order)
    # the comparison is most useful with the candidate queue of the current iteration only
    # this queue is saved in cq_satisfied
    # in theory, a refinement at the current level can be similar to a desc from an earlier level
    # this can happen for numerical and ordinal attributes, we will therefore also check the beam
    for seedcq in cq_satisfied:

        current = desc['description'].copy()
        old = seedcq['description'].copy()
        if current == old:  # we have to apply a constraint
            constraint_similar_description = True
            break

    if d_i > 1:
        for seedb in current_beam:
            current = desc['description'].copy()
            old = seedb['description'].copy()
            if current == old:  # we have to apply a constraint
                constraint_similar_description = True
                break

    return constraint_similar_description

# the min_size values are saved in general_params


def check_subgroup_size(idxIDs=None, general_params=None, sel_params=None):

    constraint_subgroup_size = False

    # we focus on proportion of rows rather than cases
    if idxIDs['size_sg_rows'] < sel_params['min_size']:
        constraint_subgroup_size = True

    return constraint_subgroup_size
