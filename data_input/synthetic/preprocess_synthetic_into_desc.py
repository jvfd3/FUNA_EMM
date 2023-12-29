import pandas as pd
import numpy as np
import string

def into_desc(ddlong=None, extra_descriptors=None, info=None):

    unique_codes = list(set(ddlong['Group'].values.codes))

    # groupby for group column
    dddesc = ddlong.groupby('IDCode').apply(desc_columns_per_case, unique_codes=unique_codes) 
    dddesc.reset_index(inplace=True)
    # check whether some variables need to be ordinal!

    # groupby for extra descriptors
    dddesc_added = add_basic_descriptors_to_desc_variant(dddesc=dddesc, extra_descriptors=extra_descriptors, info=info)

    dddesc_added_two = add_basic_descriptors_to_desc_invariant(dddesc=dddesc_added, extra_descriptors=extra_descriptors, info=info)

    info.update({'shape_desc_0': dddesc_added_two.shape[0], 'shape_desc_1': dddesc_added_two.shape[1], 'na_desc_rows': dddesc_added_two.isnull().any(axis=1).sum(), 'na_desc_overall': dddesc_added_two.isnull().sum().sum()})

    return dddesc_added_two, info

def desc_columns_per_case(x=None, unique_codes=None):

    d = {}

    #print(x)
    #seq = ''.join(x['Group'].values)
    
    cat_codes = x['Group'].values.codes
    cat_codes_plus_one = [i+1 for i in cat_codes]

    d['medgroup'] = np.round(np.median(cat_codes_plus_one),2)
    d['ungroup'] = len(list(set(cat_codes)))

    cols = ['medgroup', 'ungroup']

    for code in unique_codes:
        medtime = [i for i, value in enumerate(cat_codes) if value == code]
        letter = string.ascii_lowercase[code]

        medtime_plus_one = [i+1 for i in medtime]
        if len(medtime_plus_one) > 0: 
            d['idx'+letter] = np.median(medtime_plus_one)
        else:
            d['idx'+letter] = 0.0
        cols += ['idx'+letter]
        
        d['len'+letter] = len(medtime_plus_one)        
        cols += ['len'+letter]

    return pd.Series(d, index=cols)

def add_basic_descriptors_to_desc_variant(extra_descriptors=None, dddesc=None, info=None):

    extra_descs_var = info['extra_desc_var']
    dddesc_extra = extra_descriptors.groupby('IDCode').apply(extra_desc_columns_per_case, extra_descs_var=extra_descs_var)
    dddesc_extra.reset_index(inplace=True)

    dddesc_added = pd.merge(dddesc, dddesc_extra, how = "left")

    return dddesc_added

def add_basic_descriptors_to_desc_invariant(dddesc=None, extra_descriptors=None, info=None):

    extra_descs_invar = info['extra_desc_invar'] + ['IDCode']
    dddesc_added = pd.merge(dddesc, extra_descriptors[extra_descs_invar], how = "left")

    return dddesc_added

def extra_desc_columns_per_case(x=None, extra_descs_var=None):

    d = {}
    cols = []

    for var in extra_descs_var:
        d[var + 'mean'] = np.mean(x[var].values)
        cols.append(var + 'mean')

    return pd.Series(d, index=cols)

