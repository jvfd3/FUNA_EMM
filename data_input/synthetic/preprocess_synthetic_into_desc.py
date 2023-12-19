import pandas as pd

def into_desc(ddlong=None, info=None):

    dddesc = ddlong.groupby('IDCode').apply(desc_columns_per_case) 
    dddesc.reset_index(inplace=True)

    info.update({'shape_desc_0': dddesc.shape[0], 'shape_desc_1': dddesc.shape[1], 'na_desc_rows': dddesc.isnull().any(axis=1).sum(), 'na_desc_overall': dddesc.isnull().sum().sum()})

    return dddesc, info

def desc_columns_per_case(x=None, name_task=None):

    d = {}

    # have calculated before, but easier to do it here again
    d['seq'] = ''.join(x['Group'].values)

    cols = ['seq']

    return pd.Series(d, index=cols)

