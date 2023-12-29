
import numpy as np
import pandas as pd

import beam_search.measures as me

def calculate_general_estimates(target=None, model_params=None):

    estimates = {}

    estimates = {'mean': me.calculate_mean(df=target, column=model_params['column_name']), 'mean_se': me.calculate_mean_se(df=target,column=model_params['column_name'])}
    qm_slope, qm_slope_se = me.calculate_slope(df=target, column=model_params['column_name'])
    estimates.update({'slope': qm_slope, 'slope_se': qm_slope_se})

    return estimates

def calculate_subgroup_estimates(target=None, model_params=None):  

    estimates = {}

    estimates = {'mean': me.calculate_mean(df=target, column=model_params['column_name']), 'mean_se': me.calculate_mean_se(df=target,column=model_params['column_name'])}
    qm_slope, qm_slope_se = me.calculate_slope(df=target, column=model_params['column_name'])
    estimates.update({'slope': qm_slope, 'slope_se': qm_slope_se})

    return estimates
