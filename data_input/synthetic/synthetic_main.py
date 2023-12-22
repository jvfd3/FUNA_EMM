import pandas as pd

import data_input.synthetic.create_basic_descriptive_target as cbdt
import data_input.synthetic.create_extra_descriptors as ced
import data_input.synthetic.preprocess_synthetic_into_wide as iw
import data_input.synthetic.preprocess_synthetic_into_desc as id
import data_input.synthetic.preprocess_synthetic_into_long as il

def generate_synthetic_data(datasets_names=None, synparams=None):

    descriptive_long, info, IDs = cbdt.create_descriptive(synparams=synparams)

    target, info = cbdt.create_targets(descriptive=descriptive_long, synparams=synparams, info=info) # dictionary of 8 target dataframes

    # create 5 time variant and 5 time invariant descriptors
    extra_descriptors, info = ced.create_extra_descriptors(dflong=descriptive_long[['IDCode','TimeInd']], synparams=synparams, info=info)

    # do something for long, wide and desc format
    long_target, info = il.into_long(ddlong=descriptive_long, extra_descriptors=extra_descriptors, info=info)
    wide_target, info = iw.into_wide(ddlong=descriptive_long, extra_descriptors=extra_descriptors, info=info)
    desc_target, info = id.into_desc(ddlong=descriptive_long, extra_descriptors=extra_descriptors, info=info)
    
    dfs = {'descriptive': descriptive_long, 'extra_descriptors': extra_descriptors, 'target': target, 'IDs': pd.DataFrame(IDs,columns=['ID']), 
           'info': pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in info.items() ]))}
    
    dfs.update({
        'desc_target': desc_target, 
        'long_target': long_target,
        'wide_target': wide_target 
    })

    return dfs

