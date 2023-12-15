
import numpy as np
import pandas as pd

import beam_search.measures as me

def calculate_general_estimates(target=None, model_params=None):

    estimates = {}

    if model_params['model'] == 'zmean':
        estimates = {'mean': me.calculate_mean(df=target, column=model_params['column_name']), 'mean_se': me.calculate_mean_se(df=target,column=model_params['column_name'])}

    return estimates

def calculate_subgroup_estimates(target=None, model_params=None):  

    estimates = {}

    if model_params['model'] == 'zmean':
        estimates = {'mean': me.calculate_mean(df=target, column=model_params['column_name']), 'mean_se': me.calculate_mean_se(df=target,column=model_params['column_name'])}
    
    return estimates
