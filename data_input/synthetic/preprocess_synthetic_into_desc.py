import pandas as pd
import numpy as np
import string

def into_desc(ddlong=None, extra_descriptors=None, info=None):

    unique_codes = list(set(ddlong['Group'].values.codes))

    dddesc = ddlong.groupby('IDCode').apply(desc_columns_per_case, unique_codes=unique_codes) 
    dddesc.reset_index(inplace=True)
    # check whether some variables need to be ordinal!

    dddesc_added = add_basic_descriptors_to_desc(ddesc=ddesc, extra_descriptors=extra_descriptors, info=info):

    info.update({'shape_desc_0': dddesc_added.shape[0], 'shape_desc_1': dddesc_added.shape[1], 'na_desc_rows': dddesc_added.isnull().any(axis=1).sum(), 'na_desc_overall': dddesc_added.isnull().sum().sum()})

    return dddesc_added, info

def desc_columns_per_case(x=None, unique_codes=None):

    d = {}

    #print(x)
    #seq = ''.join(x['Group'].values)
    
    cat_codes = x['Group'].values.codes
    cat_codes_plus_one = [i+1 for i in cat_codes]

    d['medgroup'] = np.round(np.median(cat_codes_plus_one),2)
    d['ungroups'] = len(list(set(cat_codes)))

    cols = ['medgroup', 'ungroups']

    for code in unique_codes:
        medtime = [i for i, value in enumerate(cat_codes) if value == code]
        letter = string.ascii_lowercase[code]

        medtime_plus_one = [i+1 for i in medtime]
        d['idx'+letter] = np.median(medtime_plus_one)
        cols += ['idx'+letter]
        
        d['len'+letter] = len(medtime_plus_one)        
        cols += ['len'+letter]

    return pd.Series(d, index=cols)

def add_basic_descriptors_to_desc(ddesc=None, extra_descriptors=None, info=None):

    extra_descs_invar = info['extra_desc_invar']
    extra_descs_var = info['extra_desc_var']

    ddesc_added = ddesc.copy()

    return ddesc_added

