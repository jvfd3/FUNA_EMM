import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def check_correct(x=None, name_task=None):

    d = {}

    # these are columns per case
    d[name_task + 'AnsCsum'] = x[name_task + 'AnsC'].sum()
    d[name_task + 'PreOrdmax'] = x[name_task + 'PreOrd'].max()    
    d[name_task + 'AnsCprop'] = d[name_task + 'AnsCsum'] / d[name_task + 'PreOrdmax']

    cols = [name_task + 'AnsCsum', name_task + 'PreOrdmax', name_task + 'AnsCprop']

    return pd.Series(d, index=cols)

def retrieve_basic_descriptor_information(x):

    d = {}
    d['IDCode'] = "".join(item for item in x)
    d['sex'] = x[0]
    d['grade'] = x[1]
    d['language'] = x[2]
    
    return pd.Series(d, index=['IDCode', 'sex', 'grade', 'language'])

def check_suitable_as_target(x=None):

    # symbol + nonsymbolic the same + answer correct
    x['DMSameC'] = np.where((x['DMcor'].values == 1) & (x['DMAnsC'].values == 1), 1, 0)

    subset = x[x['DMSameC'] == 1] # this includes both the number the same and the answer correct

    # cases should have at least one answer on all 1-9 values
    if subset['DMStimL'].nunique() == 9:        
        return subset[['IDCode', 'DMStimL', 'DMTime']]
    else:
        return None

def desc_columns_per_case(x=None, name_task=None):

    d = {}

    # have calculated before, but easier to do it here again
    d[name_task + 'AnsCsum'] = x[name_task + 'AnsC'].sum()
    d[name_task + 'PreOrdmax'] = x[name_task + 'PreOrd'].max()    
    d[name_task + 'AnsCprop'] = d[name_task + 'AnsCsum'] / d[name_task + 'PreOrdmax']

    d[name_task + 'timeCmean'] = x.loc[x[name_task + 'AnsC'] == 1, name_task + 'Time'].mean()
    d[name_task + 'timeCmedian'] = x.loc[x[name_task + 'AnsC'] == 1, name_task + 'Time'].median()
    d[name_task + 'IES'] = d[name_task + 'timeCmedian'] / d[name_task + 'AnsCprop']
    
    cols = [name_task + 'AnsCsum', name_task + 'PreOrdmax', name_task + 'AnsCprop', name_task + 'timeCmean', name_task + 'timeCmedian', name_task + 'IES']

    if name_task == 'NC':

        subset = x[x[name_task + 'AnsC'] == 1]
        if subset.shape[0] > 0:
            RTslope, RTintercept = calculate_RT_slopes(name_task=name_task, x=subset, t='NumDis')
            d[name_task + 'RTslopeNumDis'] = RTslope
            d[name_task + 'RTinterceptNumDis'] = RTintercept

            RTslope, RTintercept = calculate_RT_slopes(name_task=name_task, x=subset, t='NumRatio')
            d[name_task + 'RTslopeNumRatio'] = RTslope
            d[name_task + 'RTinterceptNumRatio'] = RTintercept           
        else: 
            d[name_task + 'RTslopeNumDis'] = np.nan
            d[name_task + 'RTinterceptNumDis'] = np.nan
            d[name_task + 'RTslopeNumRatio'] = np.nan 
            d[name_task + 'RTinterceptNumRatio'] = np.nan
        
        cols = cols + [name_task + 'RTslopeNumDis', name_task + 'RTinterceptNumDis', name_task + 'RTslopeNumRatio', name_task + 'RTinterceptNumRatio']

    return pd.Series(d, index=cols)

def calculate_RT_slopes(name_task=None, x=None, t=None):

    reg = LinearRegression().fit(x[name_task + t].values.reshape(-1,1), 
                                 x[name_task + 'Time'].values.reshape(-1,1))

    RTslope = reg.coef_[0][0]
    RTintercept = reg.intercept_[0]

    return RTslope, RTintercept

def find_max_and_expand(df=None):

    # find max
    maxT = df.groupby('IDCode')['IDCode'].count()
    
    # make new t column
    newT = maxT.apply(lambda x: np.arange(1,x+1))
    df['PreOrd'] = newT.explode().values   
    
    return df
    

    
