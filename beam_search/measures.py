import numpy as np
import pandas as pd

def calculate_mean(df=None, column=None):

    qm_mean = df[column].mean()

    return np.round(qm_mean, 4)

def calculate_mean_se(df=None, column=None):

    qm_se = df[column].std(axis=0) / np.sqrt(df.shape[0])

    return np.round(qm_se, 4)

def calculate_slope(df=None, column=None):

    # average slope per ID
    avgslopes = df.groupby('IDCode').apply(calculate_slope_per_id, column=column)
    avgslopes.reset_index(inplace=True)
    
    # sort such that timepoint 10 is later than 2
    avgslopes['IDNumber'] = avgslopes['IDCode'].str[2:].astype(int)    
    avgslopes_sorted = avgslopes.sort_values(by=['IDNumber'])

    qm_slope = avgslopes_sorted['avgslope'].mean()
    qm_slope_se = avgslopes_sorted['avgslope'].std() / np.sqrt(avgslopes_sorted.shape[0])

    return np.round(qm_slope, 4), np.round(qm_slope_se, 4)

def calculate_slope_per_id(x=None, column=None):

    d = {}

    vals = x[column].values

    if len(vals) > 1:
        slopes = vals[1:] - vals[:-1]
        d['avgslope'] = np.mean(slopes)
    else:
        d['avgslope'] = 0

    cols = ['avgslope']

    return pd.Series(d, index=cols)
