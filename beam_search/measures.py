import numpy as np
import pandas as pd

import experiment.pwlf as pwlf

def calculate_mean(df=None, column=None):

    qm_mean = df[column].mean()

    return np.round(qm_mean, 4)

def calculate_mean_se(df=None, column=None):

    qm_se = df[column].std(axis=0) / np.sqrt(df.shape[0])

    return np.round(qm_se, 4)

def calculate_slope(df=None, columns=None):

    val_col = columns[0]
    id_col = columns[1]
    time_col = columns[2]

    # average slope per ID
    avgslopes = df.groupby(id_col).apply(calculate_slope_per_id, val_column=val_col, time_column=time_col)
    avgslopes.reset_index(inplace=True)
    
    # sort such that timepoint 10 is later than 2
    #avgslopes['IDNumber'] = avgslopes[id_col].str[2:].astype(int)    
    #avgslopes_sorted = avgslopes.sort_values(by=['IDNumber'])

    qm_slope = avgslopes['avgslope'].mean()
    qm_slope_se = avgslopes['avgslope'].std() / np.sqrt(avgslopes.shape[0])

    return np.round(qm_slope, 4), np.round(qm_slope_se, 4)

def calculate_slope_per_id(x=None, val_column=None, time_column=None):

    d = {}

    x_sorted = x.sort_values(by=[time_column])

    vals = x_sorted[val_column].values
    timepoints = x_sorted[time_column].values

    if len(vals) > 1:
        difs = vals[1:] - vals[:-1]
        steps = timepoints[1:] - timepoints[:-1]
        slopes = difs / steps
        d['avgslope'] = np.mean(slopes)
    else:
        d['avgslope'] = 0

    cols = ['avgslope']

    return pd.Series(d, index=cols)

def calculate_subrange(df=None, columns=None):

    xaxis = columns[3]
    yaxis = columns[0]

    xx = df[xaxis].values
    yy = df[yaxis].values

    i = 1
    while i > 0:
        my_pwlf = pwlf.PiecewiseLinFit(xx, yy)
        res = my_pwlf.fitfast(2, pop = 2) # 2 line segments, # 2 initializations
        fitbreaks = my_pwlf.fit_breaks
        if fitbreaks[1] > 2: # sub range under 2 likely means that the algorithm has not run properly, however, could it also mean that there is no subitizing range? 
            i = 0
        else:
            i -= 0.2 # maximum 5 tries
        if i == 0:
            print(fitbreaks)
        
    #print(type(fitbreaks))
    #print(fitbreaks.shape)
    #print(fitbreaks[1])
    slopes = my_pwlf.calc_slopes() # this function calculates the regression slopes of the two segments
    # the change in regression slope (beta) should be used to calculate the standard error of the breakpoint
    # beta2 = slopes[1] - slopes[0]
    #print('slopes:', slopes) # two slopes of two segments
    #print('beta:', my_pwlf.beta) # 3 beta values:beta0 = intercept in data at x=1 = intercept[0] + beta1, beta1 = first slope, beta2 = difference in two slopes
    betas = my_pwlf.beta
    intercepts = my_pwlf.intercepts
    #print(intercepts)
    #print('intercepts:', my_pwlf.intercepts) # two intercepts of two segments, intercept[0] is real connection to y-axis at x=0

    #intercepts = yhat[0:-1] - my_pwlf.calc_slopes() * my_pwlf.fit_breaks[0:-1]
    #print('intercepts': intercepts) # just to check

    #print('ses linear:', my_pwlf.standard_errors(method='linear'))
    my_pwlf.standard_errors(method='non-linear')
    #print('ses non linear:', errors)
    # not needed since method = non-linear in the my_pwlf package give the same result
    #se, params = my_pwlf.calc_standard_errors_fit_breaks()
    #print('se:' , se)
    #print('params:', params)    
    ses = my_pwlf.se
    #print(ses) # four values... 
    ssr = my_pwlf.ssr

    qm_subrange = np.round(fitbreaks[1],2) # 1 value
    qm_subrange_se = np.round(ses[3],2) # 1 value

    qm_slopes = np.round(slopes,2) # 2 values
    qm_intercepts = np.round(intercepts,2) # 2 values
    qm_fitbreaks = np.round(fitbreaks,2) # 3 values
    qm_betas = np.round(betas,2) # 3 values
    
    #qm_subrange_ssr = np.round(ssr,2) # 1 value
    #qm_subrange_fit = np.round(np.sum(dferror['yerror']**2)/len(yy),2)

    return qm_subrange, qm_subrange_se, qm_slopes, qm_intercepts, qm_fitbreaks, qm_betas

def calculate_error_subrange(df=None, estimates=None, columns=None, general_params=None):

    # here, we calculate the global error and local error of the subgroup rows 
    
    # we first have to re-scale the data to work with the hinge function
    # start with global data
    xx = df[columns[3]].values
    yy = df[columns[0]].values
    my_pwlf = pwlf.PiecewiseLinFit(xx, yy)
    Ad = my_pwlf.assemble_regression_matrix(general_params['estimates']['fitbreaks'], my_pwlf.x_data)
    yhat = np.dot(Ad, general_params['estimates']['betas']) 
    errors = yy - yhat
    global_error = np.round(np.sum(errors**2)/len(yy),2)

    # continue with local data
    # xx and yy are the same, the estimates are different
    my_pwlf = pwlf.PiecewiseLinFit(xx, yy)
    Ad = my_pwlf.assemble_regression_matrix(estimates['fitbreaks'], my_pwlf.x_data)
    yhat = np.dot(Ad, estimates['betas']) 
    errors = yy - yhat
    local_error = np.round(np.sum(errors**2)/len(yy),2)

    return global_error, local_error
