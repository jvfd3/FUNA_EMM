import pandas as pd

import data_input.synthetic.create_basic_descriptive_target as cbdt
import data_input.synthetic.preprocess_synthetic_into_wide as iw
import data_input.synthetic.preprocess_synthetic_into_desc as id

def generate_synthetic_data(datasets_names=None, synparams=None):

    descriptive_long, info, IDs = cbdt.create_descriptive(synparams=synparams)

    target, info = cbdt.create_targets(descriptive=descriptive_long, info=info) # dictionary of 8 target dataframes

    # do something for long, wide and desc format
    wide_target, info = iw.into_wide(ddlong=descriptive_long, info=info)
    desc_target, info = id.into_desc(ddlong=descriptive_long, info=info)
    
    dfs = {'descriptive': descriptive_long, 'target': target, 'IDs': pd.DataFrame(IDs,columns=['ID']), 'info': pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in info.items() ]))}
    
    dfs.update({
        'desc_target': desc_target, 
        'long_target': descriptive_long,
        'wide_target': wide_target 
    })

    return dfs

