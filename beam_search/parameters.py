
import numpy as np
import pandas as pd

import beam_search.measures as me

def calculate_general_estimates(target=None, sel_params=None, extra_info=None):

    estimates = {}
    if "wra" in sel_params['model']:
        if extra_info['case_based_target']:
            longtarget = target.copy()
            target = longtarget.groupby(extra_info['target_column_names'][1]).first()
        qm_p = me.calculate_support_class(df=target, column=extra_info['target_column_names'][0], prefclass=extra_info['prefclass'])
        estimates = {'suppclass': qm_p}
    if "zmean" in sel_params['model']: 
        qm_mean = me.calculate_mean(df=target, column=extra_info['target_column_names'][0])
        qm_mean_se = me.calculate_mean_se(df=target, column=extra_info['target_column_names'][0])
        estimates = {'mean_est': qm_mean, 'mean_se': qm_mean_se}
    if "zslope" in sel_params['model']: 
        qm_slope, qm_slope_se = me.calculate_slope(df=target, columns=extra_info['target_column_names'])
        estimates = {'slope_est': qm_slope, 'slope_se': qm_slope_se}
    if "subrange" in sel_params['model']:
        qm_subrange, qm_subrange_se, qm_slopes, qm_intercepts, qm_fitbreaks, qm_betas = me.calculate_subrange(df=target, columns=extra_info['target_column_names'])
        estimates = {'subrange_est': qm_subrange, 'subrange_se': qm_subrange_se, 'slopes': qm_slopes, 'intercepts': qm_intercepts, 
                     'fitbreaks': qm_fitbreaks, 'betas': qm_betas}

    return estimates

def calculate_subgroup_estimates(target=None, sel_params=None, extra_info=None, general_params=None):  

    #estimates = {'sgsize': len(target)}
    estimates = {}

    if "wra" in sel_params['model']:
        qm_p = me.calculate_support_class(df=target, column=extra_info['target_column_names'][0], prefclass=extra_info['prefclass'])
        estimates = {'suppclass': qm_p}
    if "zmean" in sel_params['model']: 
        qm_mean = me.calculate_mean(df=target, column=extra_info['target_column_names'][0])
        qm_mean_se = me.calculate_mean_se(df=target,column=extra_info['target_column_names'][0])
        estimates = {'mean_est': qm_mean, 'mean_se': qm_mean_se}
    if "zslope" in sel_params['model']: 
        qm_slope, qm_slope_se = me.calculate_slope(df=target, columns=extra_info['target_column_names'])
        estimates = {'slope_est': qm_slope, 'slope_se': qm_slope_se}
    if "subrange" in sel_params['model']:
        qm_subrange, qm_subrange_se, qm_slopes, qm_intercepts, qm_fitbreaks, qm_betas = me.calculate_subrange(df=target, columns=extra_info['target_column_names'])
        estimates = {'subrange_est': qm_subrange, 'subrange_se': qm_subrange_se, 'slopes': qm_slopes, 'intercepts': qm_intercepts, 
                     'fitbreaks': qm_fitbreaks, 'betas': qm_betas}    
    if sel_params['model'] == 'subrange_fit':
        global_error, local_error = me.calculate_error_subrange(df=target, estimates=estimates, columns=extra_info['target_column_names'], general_params=general_params)
        estimates.update({'global_error': global_error, 'local_error': local_error})

    estimates.update({'nrrows':len(target)})

    return estimates
