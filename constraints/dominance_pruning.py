import numpy as np
import pandas as pd
import itertools as it

import beam_search.select_subgroup as ss
import beam_search.prepare_beam as pb
import beam_search.qualities as qu


def apply_dominance_pruning(result_set=None, considered_subgroups=None, sel_params=None, extra_info=None, descriptive=None, target=None, attributes=None, general_params=None):

    current_result_set = result_set.copy()
    pruned_descriptions = get_new_descriptions(result_set=result_set)

    pruned_subgroups, n_small_groups = get_new_qualities(pruned_descriptions=pruned_descriptions, descriptive=descriptive, target=target, attributes=attributes,
                                                         sel_params=sel_params, extra_info=extra_info, general_params=general_params)

    # append with result_set, to keep the original subgroups as well
    all_subgroups = [current_result_set.copy()]
    all_subgroups.append(pruned_subgroups)
    all_subgroups = [item for sublist in all_subgroups for item in sublist]

    # again apply description and cover based selection
    result_set, n_redun_descs = pb.prepare_result_set(
        candidate_result_set=all_subgroups, sel_params=sel_params, general_params=general_params)

    considered_subgroups['dominance_pruning'] = {'n_consd': len(
        pruned_descriptions), 'n_small_groups': n_small_groups, 'n_redun_decs': n_redun_descs}

    return result_set, considered_subgroups


def get_new_descriptions(result_set=None):

    pruned_descriptions = []
    for existing_subgroup in result_set:

        old_desc = existing_subgroup['description'].copy()
        items_old_desc = old_desc.items()

        for r in np.arange(1, len(list(items_old_desc))):
            combs = list(it.combinations(items_old_desc, r=r))
            combs_r = [{'description': dict(desc),
                        'adds': {'literal_order': ('dom_pruning',)}} for desc in combs]
            # print(combs_r)
            pruned_descriptions.append(combs_r)

    pruned_descriptions = [
        item for sublist in pruned_descriptions for item in sublist]

    return pruned_descriptions


def get_new_qualities(pruned_descriptions=None, descriptive=None, target=None, attributes=None, general_params=None, sel_params=None, extra_info=None):

    pruned_subgroups = []
    n_small_groups = 0

    for desc in pruned_descriptions:

        desc_qm, constraint_subgroup_size, n_small_groups = qu.evaluate_desc(desc=desc, descriptive=descriptive, attributes=attributes, target=target,
                                                                             general_params=general_params, sel_params=sel_params,
                                                                             extra_info=extra_info, n_small_groups=n_small_groups)
        if not constraint_subgroup_size:
            pruned_subgroups.append(desc_qm)

    return pruned_subgroups, n_small_groups
