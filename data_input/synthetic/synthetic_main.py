import pandas as pd

import data_input.synthetic.create_basic_descriptive_target as cbdt

def generate_synthetic_data(datasets_names=None, synparams=None):

    descriptive, info, IDs = cbdt.create_descriptive(synparams=synparams)
    target = cbdt.create_target(synparams=synparams)

    # do something for long, wide and desc format
    desc_target = transform_into_desc(descriptive=descriptive)
    long_target = transform_into_long(descriptive=descriptive)
    wide_target = transform_into_desc(descriptive=descriptive)
    
    dfs = {'descriptive': descriptive, 'target': target, 'info': pd.DataFrame(info, index=[0]), 'IDs': pd.DataFrame(IDs,columns=['ID'])}
    
    dfs.update({
        'desc_target': desc_target, 
        'long_target': long_target,
        'wide_target': wide_target 
        })

    return dfs

def transform_into_desc(descriptive=None):

    desc_target = None

    return desc_target

def transform_into_long(descriptive=None):

    long_target = None

    return long_target

def transform_into_desc(descriptive=None):

    wide_target = None

    return wide_target
