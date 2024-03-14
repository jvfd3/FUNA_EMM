import numpy as np
import pandas as pd
import random
import itertools as it

import experiment.retrieve_funa as rfuna
import experiment.retrieve_curran as rcurran 

def retrieve_rw_data(data_name=None, data_from=None, datasets_names=None, extra_info=None):

    if data_name == 'FUNA':
        dict_funa = rfuna.import_data_funa(data_name=data_name, data_from=data_from, datasets_names=datasets_names)
        descriptives, attributes, target = rfuna.retrieve_data_funa(dict=dict_funa, datasets_names=datasets_names, extra_info=extra_info) 

    if 'Curran' in data_name:
        dict_curran = rcurran.import_data_curran(data_name=data_name, data_from=data_from, datasets_names=datasets_names)
        descriptives, attributes, target = rcurran.retrieve_data_curran(dict=dict_curran, datasets_names=datasets_names) 
    '''
    for key in attributes.keys():
        print(key)
        print(sum(len(v) for v in attributes[key].values()))
        #print(attributes[key].values())    
    for desc in descriptives.keys():
        print(desc)
        data = descriptives[desc]
        print(data.shape)
        print(data.isnull().any(axis=1).sum())
        print(data.isnull().sum().sum())
    '''
    return descriptives, attributes, target



