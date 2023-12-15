import pandas as pd
import numpy as np
import preprocess_functions as pf

def into_long(dd=None, db=None, target=None, info=None):

    print('transform into long')

    #print(dd.keys()) # the four descriptor datasets
    #print(db.head()) # the 3 basic descriptors

    # merge
    ddmerged = merge_into_long(dd=dd)

    # add basic descriptors
    descriptive_long = pd.merge(ddmerged, db.drop_duplicates(), how = 'left') # there is only one similar column: IDCode
    info.update({'shape_long_0': descriptive_long.shape[0], 'shape_long_1': descriptive_long.shape[1], 'na_long_rows': descriptive_long.isnull().any(axis=1).sum(), 'na_long_overall': descriptive_long.isnull().sum().sum()})

    # check max length of targets and remove/extend descriptors 
    descriptive_long_checked = check_PreOrd_target(dl=descriptive_long, td=target)
    info.update({'shape_long_check_0': descriptive_long_checked.shape[0], 'shape_long_check_1': descriptive_long_checked.shape[1], 'na_long_check_rows': descriptive_long_checked.isnull().any(axis=1).sum(), 'na_long_check_overall': descriptive_long_checked.isnull().sum().sum()})

    return descriptive_long_checked, descriptive_long, info

def merge_into_long(dd=None):

    # start with NC
    data = dd['NC'].copy()
    data['PreOrd'] = data['NCPreOrd']
    data.drop(['NCPreOrd'], axis=1, inplace=True)

    for key in dd.keys():
        if not key == 'NC':
            adddata = dd[key].copy()
            data = pd.merge(data, adddata, how = 'outer', left_on=['IDCode','PreOrd'], right_on=['IDCode',key+'PreOrd'], suffixes=('', '_y'))
            data.drop(data.filter(regex='_y$').columns, axis=1, inplace=True) 
            
            data = data.sort_values(by=['IDCode','PreOrd',key+'PreOrd']).reset_index(drop=True)
            data.drop(['PreOrd',key+'PreOrd'], axis=1, inplace=True)

            # find the max t value per case and expand
            data = pf.find_max_and_expand(data)             

    return data

def check_PreOrd_target(dl=None, td=None):
  
    maxT_target = td.groupby(['IDCode'])['IDCode'].count()
    maxT_desc = dl.groupby(['IDCode'])['IDCode'].count()

    # for funa, the target data is much shorter than the descriptive data
    # this has direct effect on the missing data method that will be used
    # for other datasets, we may have to add extra rows in the descriptive data

    extra_rows_desc = maxT_target - maxT_desc # extra rows needed in desc
    IDs_need_extra_rows = extra_rows_desc[extra_rows_desc > 0] # for funa, 0 cases
    if len(IDs_need_extra_rows) > 0:
        print('!need to add extra rows!')
        # still needs to be done
        descriptive_long = dl.copy()
    else:
        print('!need to remove rows!')
        IDs_rows_to_be_removed = abs(extra_rows_desc[extra_rows_desc < 0])
        keep_items = maxT_desc.subtract(IDs_rows_to_be_removed, fill_value=0)
        dlm = dl.merge(keep_items.rename('keep_items'),how='left',left_on='IDCode',right_index=True)
        descriptive_long = dlm[dlm['PreOrd'] <= dlm['keep_items']].drop(['keep_items'],axis=1)

    return descriptive_long