import pandas as pd

import data_input.synthetic.create_basic_descriptive_target as cbdt

def generate_synthetic_data(datasets_names=None, synparams=None):

    descriptive, info, IDs = cbdt.create_descriptive(synparams=synparams)

    target, info = cbdt.create_targets(descriptive=descriptive, info=info) # dictionary of 8 target dataframes

    # do something for long, wide and desc format
    #desc_target = transform_into_desc(descriptive=descriptive)
    #long_target = transform_into_long(descriptive=descriptive)
    #wide_target = transform_into_desc(descriptive=descriptive)
    
    dfs = {'descriptive': descriptive, 'target': target, 'IDs': pd.DataFrame(IDs,columns=['ID'])}
    
    dfs.update({
        'desc_target': descriptive, 
        'long_target': descriptive,
        'wide_target': descriptive 
    })

    return dfs

def transform_into_desc(descriptive=None):

    desc_target = pd.DataFrame()

    return desc_target

def transform_into_long(descriptive=None):

    long_target = pd.DataFrame()

    return long_target

def transform_into_desc(descriptive=None):

    wide_target = pd.DataFrame()

    return wide_target
