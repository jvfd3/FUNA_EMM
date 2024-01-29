import pandas as pd
import numpy as np
import string

def into_desc(ddlong=None, extra_descriptors=None, info=None):

    unique_codes = list(set(ddlong['Group'].values.codes))
    un_cat_codes_plus_one = [i+1 for i in unique_codes]
    meanval = np.mean(un_cat_codes_plus_one)
    meanidx = np.max(ddlong['TimeInd'].values)/2

    # groupby for group column
    dddesc = ddlong.groupby('IDCode').apply(desc_columns_per_case, unique_codes=unique_codes, meanval=meanval, meanidx=meanidx) 
    dddesc.reset_index(inplace=True)
    # check whether some variables need to be ordinal!

    # groupby for extra descriptors
    dddesc_added = add_basic_descriptors_to_desc_variant(dddesc=dddesc, extra_descriptors=extra_descriptors, info=info)

    dddesc_added_two = add_basic_descriptors_to_desc_invariant(dddesc=dddesc_added, extra_descriptors=extra_descriptors, info=info)

    info.update({'shape_desc_0': dddesc_added_two.shape[0], 'shape_desc_1': dddesc_added_two.shape[1], 'na_desc_rows': dddesc_added_two.isnull().any(axis=1).sum(), 'na_desc_overall': dddesc_added_two.isnull().sum().sum()})

    return dddesc_added_two, info

def desc_columns_per_case(x=None, unique_codes=None, meanval=None, meanidx=None):

    d = {}

    #print(x)
    #seq = ''.join(x['Group'].values)
    
    cat_codes = x['Group'].values.codes
    cat_codes_plus_one = [i+1 for i in cat_codes]

    #d['medgroup'] = np.round(np.median(cat_codes_plus_one),2)
    #d['ungroup'] = len(list(set(cat_codes)))
    #d['difgroup'] = cat_codes_plus_one[-1] - cat_codes_plus_one[0]
    
    # create perfect description model, depends on the subgroup type
    subgroups = ['A', 'B', 'C', 'D'] + ['E', 'F', 'G', 'H']
    cols = []

    for sgtype in subgroups:
        dist = calculate_delta(cat_codes=cat_codes, sgtype=sgtype, meanval=meanval, meanidx=meanidx)     
        d['sum'+sgtype] = np.sum(dist)
        d['dif'+sgtype] = dist[-1] - dist[0]
        cols += ['sum'+sgtype, 'dif'+sgtype]

    for code in unique_codes:
        medtime = [i for i, value in enumerate(cat_codes) if value == code]
        letter = string.ascii_lowercase[code]

        medtime_plus_one = [i+1 for i in medtime]
        if len(medtime_plus_one) > 0: 
            d['idx'+letter] = np.median(medtime_plus_one)
        else:
            d['idx'+letter] = 0.0
        cols += ['idx'+letter]
        
        d['freq'+letter] = len(medtime_plus_one)        
        cols += ['freq'+letter]

    return pd.Series(d, index=cols)

def calculate_delta(cat_codes=None, sgtype=None, meanval=None, meanidx=None):

    alpha = 0
    beta = 0
    gamma = 0
    if sgtype == 'B':
        alpha = 1.0
    if sgtype == 'C':
        beta = 1.0
    if sgtype == 'D':
        alpha = 1.0
        beta = 1.0
    if sgtype == 'E':
        gamma = 1.0
    if sgtype == 'F':
        gamma = 1.0
        alpha = 1.0
    if sgtype == 'G': 
        gamma = 1.0
        beta = 1.0
    if sgtype == 'H':
        alpha = 1.0
        beta = 1.0
        gamma = 1.0      

    dist = [(alpha*(idx+1-meanidx)) + (beta*(val+1-meanval)) + (gamma*(val+1-meanval)*(idx+1-meanidx)) for idx,val in enumerate(cat_codes)]

    return dist

def add_basic_descriptors_to_desc_variant(extra_descriptors=None, dddesc=None, info=None):

    extra_descs_var = info['extra_desc_var']
    dddesc_extra = extra_descriptors.groupby('IDCode').apply(extra_desc_columns_per_case, extra_descs_var=extra_descs_var)
    dddesc_extra.reset_index(inplace=True)

    dddesc_added = pd.merge(dddesc, dddesc_extra, how = "left")

    return dddesc_added

def add_basic_descriptors_to_desc_invariant(dddesc=None, extra_descriptors=None, info=None):

    extra_descs_invar = info['extra_desc_invar'] + ['IDCode']
    dddesc_added = pd.merge(dddesc, extra_descriptors[extra_descs_invar].drop_duplicates(), how = "left")

    return dddesc_added

def extra_desc_columns_per_case(x=None, extra_descs_var=None):

    d = {}
    cols = []

    for var in extra_descs_var:
        d[var + 'mean'] = np.mean(x[var].values)
        cols.append(var + 'mean')

    return pd.Series(d, index=cols)

