import numpy as np
import pandas as pd
import random as r
from joblib import Parallel, delayed

import beam_search.beam_search as bs

def distribution_false_discoveries_params(m=None, target=None, attributes=None, descriptive=None, sel_params=None, extra_info=None):

    sel_params_temp = sel_params.copy()
    sel_params_temp['q'] = 1

    # make list with varphi values
    distribution = make_distribution_false_discoveries(m=m, target=target, attributes=attributes, descriptive=descriptive, sel_params_temp=sel_params_temp, extra_info=extra_info)

    return distribution

def make_distribution_false_discoveries(m=None, target=None, attributes=None, descriptive=None, sel_params_temp=None, extra_info=None):

    inputs = range(m)
    print('building distribution of false discoveries...')

    qm_values = Parallel(n_jobs=-2)(delayed(make_false_discovery)(i, target, attributes, descriptive, sel_params_temp, extra_info) for i in inputs)

    return qm_values

def make_false_discovery(i=None, target=None, attributes=None, descriptive=None, sel_params_temp=None, extra_info=None):

    print(i)

    shuffled_descriptive = shuffle_dataset(descriptive=descriptive, attributes=attributes)

    # perform beam search    
    result_emm, general_params, considered_subgroups = bs.beam_search(target=target, attributes=attributes, descriptive=shuffled_descriptive, sel_params=sel_params_temp, extra_info=extra_info)

    # save qm of the first subgroup
    #print(result_emm)
    qm_value = result_emm['varphi'].values[0] 

    return qm_value

def shuffle_dataset(descriptive=None, attributes=None):

    # this function is important in the context of wide and long targets
    # currently, target data is selected based on ID and time counter
    # it is thus necessary to swap these columns, rather than changing the indices
    id_atts = attributes['id_atts']

    tobe_shuffled_descriptive = descriptive.copy()
    tobe_shuffled_descriptive.reset_index(inplace=True,drop=True)
    tobe_shuffled_descriptive.drop(id_atts,axis=1,inplace=True)
    idx = np.arange(0, len(descriptive))
    
    new_idx = idx.copy()
    r.shuffle(new_idx)

    # remove ID columns and shuffle    
    shuffled_descriptive = tobe_shuffled_descriptive.loc[new_idx]
    shuffled_descriptive.reset_index(inplace=True,drop=True)

    # add ID columns
    shuffled_descriptive[id_atts[0]] = descriptive[id_atts[0]]
    if len(id_atts) == 2:
        shuffled_descriptive[id_atts[1]] = descriptive[id_atts[1]]

    return shuffled_descriptive