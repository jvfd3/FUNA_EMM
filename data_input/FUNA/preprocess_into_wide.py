import pandas as pd
import numpy as np
import preprocess_functions as pf

def into_wide(ddlong=None, ddlongchecked=None, db=None, info=None):

    print('transform into wide')

    descriptive_wide = change_into_wide(ddlong=ddlong, db=db)
    info.update({'shape_wide_0': descriptive_wide.shape[0], 'shape_wide_1': descriptive_wide.shape[1], 'na_wide_rows': descriptive_wide.isnull().any(axis=1).sum(), 'na_wide_overall': descriptive_wide.isnull().sum().sum()})
    
    ddwide10, ddwide50, ddwide90, info = remove_columns_based_on_missings(descriptive_wide, info)  

    descriptive_wide_adapt_to_target = change_into_wide(ddlong=ddlongchecked, db=db)
    info.update({'shape_wide_adapt_0': descriptive_wide_adapt_to_target.shape[0], 'shape_wide_adapt_1': descriptive_wide_adapt_to_target.shape[1], 
                 'na_wide_adapt_rows': descriptive_wide_adapt_to_target.isnull().any(axis=1).sum(), 
                 'na_wide_adapt_overall': descriptive_wide_adapt_to_target.isnull().sum().sum()})
    #descriptive_wide_adapt_to_target, info = wide_with_18_timepoints(ddlong, db, info)    

    return descriptive_wide, info, ddwide10, ddwide50, ddwide90, descriptive_wide_adapt_to_target

def change_into_wide(ddlong=None, db=None):

    # start from ddlong
    # change into wide format and add the 1 : maxT to every column
    ddlong = ddlong.drop([
        'sex','grade','language'
        ],axis=1).copy()
    cols = ddlong.drop(['IDCode','PreOrd'],axis=1).columns.values
    ddwide = ddlong.pivot(index='IDCode',columns='PreOrd',values=cols)
    # ddwide.columns.values are now tuples

    ddwide = check_for_completely_NA(ddwide)    

    descriptive_wide = remove_multi_index(ddwide)

    descriptive_wide = add_basic_descriptors(descriptive_wide, db)

    return descriptive_wide

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

def add_basic_descriptors(descriptive_wide=None, db=None):

    # add basic descriptors
    descriptive_wide = pd.merge(descriptive_wide, db.drop_duplicates(), how = 'left') # there is only one similar column: IDCode

    return descriptive_wide

def remove_columns_based_on_missings(descriptive_wide=None, info=None):

    # remove descriptors with too many missing values
    # we make three thresholds: every column should have at least >0 (descriptive_wide), 10%, 50% or 90% of the values (= not more than 100\%, 90%, 50% or 10% missing)
    nr_rows = descriptive_wide.shape[0]
    keep_cols10 = descriptive_wide.columns.values[descriptive_wide.isnull().sum() <= 0.9*nr_rows]
    ddwide10 = descriptive_wide[keep_cols10]
    info.update({'shape_wide10_0': ddwide10.shape[0], 'shape_wide10_1': ddwide10.shape[1], 'na_wide10_rows': ddwide10.isnull().any(axis=1).sum(), 'na_wide10_overall': ddwide10.isnull().sum().sum()})      

    keep_cols50 = descriptive_wide.columns.values[descriptive_wide.isnull().sum() <= 0.5*nr_rows]
    ddwide50 = descriptive_wide[keep_cols50]
    info.update({'shape_wide50_0': ddwide50.shape[0], 'shape_wide50_1': ddwide50.shape[1], 'na_wide50_rows': ddwide50.isnull().any(axis=1).sum(), 'na_wide50_overall': ddwide50.isnull().sum().sum()})    

    keep_cols90 = descriptive_wide.columns.values[descriptive_wide.isnull().sum() <= 0.1*nr_rows]
    ddwide90 = descriptive_wide[keep_cols90]
    info.update({'shape_wide90_0': ddwide90.shape[0], 'shape_wide90_1': ddwide90.shape[1], 'na_wide90_rows': ddwide90.isnull().any(axis=1).sum(), 'na_wide90_overall': ddwide90.isnull().sum().sum()})  

    return ddwide10, ddwide50, ddwide90, info

