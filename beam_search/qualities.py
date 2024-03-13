import numpy as np
import math

import beam_search.parameters as pa
import beam_search.select_subgroup as ss
import constraints.constraints as cs

def evaluate_desc(desc=None, descriptive=None, attributes=None, target=None, sel_params=None, extra_info=None, general_params=None, n_small_groups=None):

    #print('desc', desc)
    desc_qm = None

    subgroup, idxIDs, subgroup_compl, idx_compl = ss.select_subgroup(description=desc['description'], df=descriptive, attributes=attributes)
                    
    constraint_subgroup_size = cs.check_subgroup_size(idxIDs=idxIDs, general_params=general_params, sel_params=sel_params)
    if constraint_subgroup_size:
        n_small_groups += 1
    else: 
        subgroup_params = calculate_subgroup_params(target=target, sel_params=sel_params, extra_info=extra_info, general_params=general_params, idxIDs=idxIDs)                                              
        desc_qm = add_qm(desc=desc, general_params=general_params, subgroup_params=subgroup_params) 
    
    return desc_qm, constraint_subgroup_size, n_small_groups

def calculate_general_params(target=None, sel_params=None, extra_info=None):

    estimates = pa.calculate_general_estimates(target=target, sel_params=sel_params, extra_info=extra_info)
    general_params = {'IDs': list(target[extra_info['target_column_names'][1]].unique()), 'nrrows': target.shape[0], 'estimates': estimates}

    return general_params

def calculate_subgroup_params(target=None, sel_params=None, extra_info=None, general_params=None, idxIDs=None):
    
    seltarget = ss.select_subgroup_part_of_target(idxIDs=idxIDs, target=target, case_based_target=extra_info['case_based_target'])
    estimates = pa.calculate_subgroup_estimates(target=seltarget, sel_params=sel_params, extra_info=extra_info, general_params=general_params, idxIDs=idxIDs)    
    varphi = calculate_varphi(estimates=estimates, sel_params=sel_params, general_params=general_params)    
    subgroup_params = {'idxIDs': idxIDs, 'estimates': estimates, 'varphi': varphi, 'temp_varphi': float('-inf')}

    return subgroup_params

def add_qm(desc=None, general_params=None, subgroup_params=None):

    desc_qm = desc.copy()  
    desc_qm['qualities'] = {'estimates': subgroup_params['estimates'], 'varphi': subgroup_params['varphi'], 'temp_varphi': subgroup_params['temp_varphi']}
    desc_qm['adds']['idxIDs'] = subgroup_params['idxIDs']

    return desc_qm

def calculate_varphi(estimates=None, sel_params=None, general_params=None, idxIDs=None):

    varphi = np.nan

    if sel_params['model'] == 'wra':
        varphi = np.round((estimates['nrrows']/general_params['nrrows'])*(estimates['suppclass']-general_params['estimates']['suppclass']),4)

    if sel_params['model'] in ['zmean','zmean_high']:
        if estimates['mean_se'] > 0:
            if sel_params['model'] == 'zmean': # absolute
                varphi = np.round(np.abs(estimates['mean_est'] - general_params['estimates']['mean_est']) / estimates['mean_se'],1)
            elif sel_params['model'] == 'zmean_high': # one-sided, large
                varphi = np.round((estimates['mean_est'] - general_params['estimates']['mean_est']) / estimates['mean_se'],1)
        else:
            varphi = 0
    
    if sel_params['model'] == 'zslope_high': # one-sided
        if estimates['slope_se'] > 0: 
            varphi = np.round((estimates['slope_est'] - general_params['estimates']['slope_est']) / estimates['slope_se'],1)
        else:
            varphi = 0

    if sel_params['model'] in ['reg_ssr', 'reg_ssrb', 'reg_bic']:
        n = estimates['nrrows']        
        N = general_params['nrrows']
        nc = N - n
        if nc == 0:
            varphi = float('-inf')
        else:
            ef = -((n/N)*math.log((n/N),2)) - ((nc/N)*math.log((nc/N),2))
            A = estimates['SSresLocal']             
            B = estimates['SSresGlobal']
            if sel_params['model'] == 'reg_ssr':
                varphi = np.round(-1*((1/ef)*(A/n)), 2)      
            if sel_params['model'] == 'reg_ssrb':
                varphi = np.round(ef * (A/n) * ((B/n)-(A/n)), 2)  
            if sel_params['model'] == 'reg_bic':
                varphi = np.round((-1*n*np.log(A/n))-(estimates['nrparams']*np.log(n))-(-1*n*np.log(B/n))+(general_params['estimates']['nrparams']*np.log(n)),2)

    if sel_params['model'] == 'zsubrange_low': # one-sided, small
        if estimates['subrange_se'] > 0:
            varphi = np.round(-(estimates['subrange_est'] - general_params['estimates']['subrange_est']) / estimates['subrange_se'],1)            
        else: 
            varphi = 0
    if sel_params['model'] == 'zsubrange_high': # one-sided, small
        if estimates['subrange_se'] > 0:
            varphi = np.round((estimates['subrange_est'] - general_params['estimates']['subrange_est']) / estimates['subrange_se'],1)
        else:
            varphi = 0
    
    if sel_params['model'] in ['subrange_fit', 'subrange_ssr', 'subrange_ssrb', 'subrange_ll', 'subrange_bic']: 
        n = estimates['nrrows']        
        N = general_params['nrrows']
        nc = N - n
        if nc == 0:
            varphi = float('-inf')
        else:
            ef = -((n/N)*math.log((n/N),2)) - ((nc/N)*math.log((nc/N),2))
            A = estimates['SSresLocal']             
            B = estimates['SSresGlobal']
            if sel_params['model'] == 'subrange_fit':                
                varphi = np.round(ef * ((B/n)-(A/n)), 2)
            if sel_params['model'] == 'subrange_ssr':
                #varphi = np.round(ef * -1 * (A/n), 2)     
                varphi = np.round(-1*((1/ef)*(A/n)), 2)      
            #if sel_params['model'] == 'subrange_ssrs':
            #    varphi = np.round(-1 * (A/n), 2)                 
            if sel_params['model'] == 'subrange_ssrb':
                varphi = np.round(ef * (A/n) * ((B/n)-(A/n)), 2)
            if sel_params['model'] in ['subrange_ll', 'subrange_bic']:
                llA = (n/2)*np.log(estimates['precision']) - (n/2)*np.log(2*np.pi) - 0.5*(estimates['precision'])*A
                llB = (n/2)*np.log(general_params['estimates']['precision']) - (n/2)*np.log(2*np.pi) - 0.5*(general_params['estimates']['precision'])*B
                if sel_params['model'] == 'subrange_ll':
                    varphi = np.round(llA-estimates['nrparams']-llB+general_params['estimates']['nrparams'], 2)
                elif sel_params['model'] == 'subrange_bic': 
                    varphi = np.round((-1*n*np.log(A/n))-(estimates['nrparams']*np.log(n))-(-1*n*np.log(B/n))+(general_params['estimates']['nrparams']*np.log(n)),2)

    return varphi
