import pandas as pd
import numpy as np

def into_wide(ddlong=None, extra_descriptors=None, info=None):

    # start from ddlong
    # change into wide format and add the 1 : maxT to every column
    cols = ddlong.drop(['IDCode','TimeInd'],axis=1).columns.values
    ddwide = ddlong.pivot(index='IDCode',columns='TimeInd',values=cols)
    # ddwide.columns.values are now tuples

    ddwide = check_for_completely_NA(ddwide=ddwide)    
    descriptive_wide = remove_multi_index(ddwide=ddwide)
    descriptive_wide_cat = add_category_type(descriptive_wide=descriptive_wide)    

    descriptive_wide_cat_added = add_basic_descriptors_to_wide(ddwide=descriptive_wide_cat, extra_descriptors=extra_descriptors, info=info)

    info.update({'shape_wide_0': descriptive_wide_cat_added.shape[0], 'shape_wide_1': descriptive_wide_cat_added.shape[1], 'na_wide_rows': descriptive_wide_cat_added.isnull().any(axis=1).sum(), 
                 'na_wide_overall': descriptive_wide_cat_added.isnull().sum().sum()})

    return descriptive_wide_cat_added, info

def check_for_completely_NA(ddwide=None):

    # check if there are columns that are completely NA, remove those columns
    keep_cols = ddwide.columns.values[ddwide.isnull().sum() != ddwide.shape[0]]
    ddwide = ddwide[keep_cols]

    return ddwide

def remove_multi_index(ddwide=None):

    descriptive_wide = ddwide.copy()
    #descriptive_wide.set_axis([c[0] + str(c[1]) for c in descriptive_wide.columns],axis='columns',inplace=True)
    #mapping = {c: c[0] + str(c[1]) for c in descriptive_wide.columns}
    #descriptive_wide.rename(columns = mapping, inplace = True)
    descriptive_wide.columns = [c[0] + str(c[1]) for c in descriptive_wide.columns.values]
    descriptive_wide.reset_index(inplace=True)

    return descriptive_wide

def add_category_type(descriptive_wide=None):

    descriptive_wide_cat = descriptive_wide.copy()
    for c in descriptive_wide_cat.columns:
        descriptive_wide_cat[c] = descriptive_wide_cat[c].astype('category')

    return descriptive_wide_cat

def add_basic_descriptors_to_wide(ddwide=None, extra_descriptors=None, info=None):

    extra_descs_invar = info['extra_desc_invar']
    extra_descs_var = info['extra_desc_var']

    # do something to merge ddwide and db
    ddwide_added = ddwide.copy()

    # do this for timeinvariant descs
    #descriptive_wide = pd.merge(descriptive_wide, extra_descriptors.drop_duplicates(), how = 'left') # there is only one similar column: IDCode
    # do something else for timevariant descs

    return ddwide_added

