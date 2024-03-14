
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
    if "reg" in sel_params['model']:
        estimates = me.regression_model(df=target, columns=extra_info['target_column_names'], order=2)  
        #estimates = me.determine_model_order_reg(df=target, columns=extra_info['target_column_names'], startorder=extra_info['startorder'], maxorder=extra_info['maxorder']) 
    if "subrange" in sel_params['model']:
        estimates = me.calculate_subrange(df=target, columns=extra_info['target_column_names'], order=1)

    return estimates

def calculate_subgroup_estimates(target=None, sel_params=None, extra_info=None, general_params=None, idxIDs=None):  

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
    if "reg" in sel_params['model']:
        if 'ssr' in sel_params['model']: # to be able to repeat earlier experiments of 01022024
            estimates = me.determine_model_order_reg(df=target, columns=extra_info['target_column_names'], startorder=1, maxorder=1)  
        elif 'ssrb' in sel_params['model']: # to be able to repeat earlier experiments of 01022024
            estimates = me.determine_model_order_reg(df=target, columns=extra_info['target_column_names'], startorder=1, maxorder=1)  
        else: 
            estimates = me.determine_model_order_reg(df=target, columns=extra_info['target_column_names'], startorder=extra_info['startorder'], maxorder=extra_info['maxorder'])  
        #estimates = me.regression_model(df=target, columns=extra_info['target_column_names'])  
        SSresGlobal, SSresLocal = me.calculate_error_subrange(estimates=estimates, general_params=general_params, idxIDs=idxIDs)
        estimates.update({'SSresGlobal': SSresGlobal, 'SSresLocal': SSresLocal})
    if 'subrange' in sel_params['model']:
        if 'fit' in sel_params['model']: # to be able to repeat earlier experiments of 01022024
            estimates = me.determine_model_order(df=target, columns=extra_info['target_column_names'], startorder=1, maxorder=1)  
        else: 
            estimates = me.determine_model_order(df=target, columns=extra_info['target_column_names'], startorder=extra_info['startorder'], maxorder=extra_info['maxorder'])  
        SSresGlobal, SSresLocal = me.calculate_error_subrange(estimates=estimates, general_params=general_params, idxIDs=idxIDs)  
        estimates.update({'SSresGlobal': SSresGlobal, 'SSresLocal': SSresLocal})

    estimates.update({'nrrows':len(target)})

    return estimates
