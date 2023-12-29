import numpy as np

import beam_search.parameters as pa
import beam_search.select_subgroup as ss
import constraints.constraints as cs

def evaluate_desc(desc=None, descriptive=None, attributes=None, target=None, model_params=None, general_params=None, alg_constraints=None, n_small_groups=None):

    #print('desc', desc)
    desc_qm = None

    subgroup, idxIDs, subgroup_compl, idx_compl = ss.select_subgroup(description=desc['description'], df=descriptive, attributes=attributes)
                    
    constraint_subgroup_size = cs.check_subgroup_size(idxIDs=idxIDs, general_params=general_params, alg_constraints=alg_constraints)
    if constraint_subgroup_size:
        n_small_groups += 1
    else: 
        subgroup_params = calculate_subgroup_params(target=target,model_params=model_params, general_params=general_params, idxIDs=idxIDs)                                              
        desc_qm = add_qm(desc=desc, general_params=general_params, subgroup_params=subgroup_params) 
    
    return desc_qm, constraint_subgroup_size, n_small_groups

def calculate_general_params(target=None, model_params=None):

    estimates = pa.calculate_general_estimates(target=target, model_params=model_params)
    general_params = {'IDs': list(target['IDCode'].unique()), 'estimates': estimates}

    return general_params

def calculate_subgroup_params(target=None, model_params=None, general_params=None, idxIDs=None):

    seltarget = ss.select_subgroup_part_of_target(idxIDs=idxIDs, target=target)

    estimates = pa.calculate_subgroup_estimates(target=seltarget, model_params=model_params)
    
    varphi = calculate_varphi(estimates=estimates, model_params=model_params, general_params=general_params)
    
    subgroup_params = {'idxIDs': idxIDs, 'estimates': estimates, 'varphi': varphi}

    return subgroup_params

def add_qm(desc=None, general_params=None, subgroup_params=None):

    desc_qm = desc.copy()  
    desc_qm['qualities'] = {'estimates': subgroup_params['estimates'], 'varphi': subgroup_params['varphi']}
    desc_qm['adds']['idxIDs'] = subgroup_params['idxIDs']

    return desc_qm

def calculate_varphi(estimates=None, model_params=None, general_params=None):

    varphi = np.nan

    if model_params['model'] == 'zmean': # absolute
        varphi = np.round(np.abs(estimates['mean'] - general_params['estimates']['mean']) / estimates['mean_se'],1)
    if model_params['model'] == 'zmean_high': # one-sided
        varphi = np.round((estimates['mean'] - general_params['estimates']['mean']) / estimates['mean_se'],1)
    if model_params['model'] == 'zslope_high': # one-sided
        if estimates['slope_se'] > 0: 
            varphi = np.round((estimates['slope'] - general_params['estimates']['slope']) / estimates['slope_se'],1)
        else:
            varphi = 0

    return varphi
