import numpy as np
import pandas as pd
import random as r
from joblib import Parallel, delayed

import beam_search.beam_search as bs

def distribution_false_discoveries_params(m=None, target=None, attributes=None, descriptive=None, sim_params=None, beam_search_params=None, model_params=None, wcs_params=None, alg_constraints=None):

    beam_search_params_temp = beam_search_params.copy()
    beam_search_params_temp['q'] = 1

    # make list with varphi values
    distribution = make_distribution_false_discoveries(m=m, target=target, attributes=attributes, descriptive=descriptive, sim_params=sim_params, beam_search_params_temp=beam_search_params_temp, model_params=model_params, wcs_params=wcs_params, alg_constraints=alg_constraints)

    return distribution

def make_distribution_false_discoveries(m=None, target=None, attributes=None, descriptive=None, sim_params=None, beam_search_params_temp=None, model_params=None, wcs_params=None, alg_constraints=None):

    inputs = range(m)
    print('building distribution of false discoveries...')

    qm_values = Parallel(n_jobs=-2)(delayed(make_false_discovery)(i, target, attributes, descriptive, sim_params, beam_search_params_temp, model_params, wcs_params, alg_constraints) for i in inputs)

    return qm_values

def make_false_discovery(i=None, target=None, attributes=None, descriptive=None, sim_params=None, beam_search_params_temp=None, model_params=None, wcs_params=None, alg_constraints=None):

    print(i)

    shuffled_descriptive = shuffle_dataset(descriptive=descriptive, attributes=attributes)

    # perform beam search    
    result_emm, general_params, considered_subgroups = bs.beam_search(target=target, attributes=attributes, descriptive=shuffled_descriptive, sim_params=sim_params, beam_search_params=beam_search_params_temp, model_params=model_params, wcs_params=wcs_params, alg_constraints=alg_constraints)

    # save qm of the first subgroup
    print(result_emm)
    qm_value = result_emm['varphi'].values[0] 

    return qm_value

def shuffle_dataset(descriptive=None, attributes=None):

    # this function is very important in the context of wide and long targets
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