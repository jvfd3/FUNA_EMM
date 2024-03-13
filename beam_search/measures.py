import numpy as np
import pandas as pd
import scipy as sc
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import experiment.pwlf as pwlf
import beam_search.select_subgroup as ss

def calculate_support_class(df=None, column=None, prefclass=None):

    seldf = df[df[column]==prefclass].copy()
    p = len(seldf)/len(df)

    return np.round(p,8)

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

def regression_model(df=None, columns=None, order=1):

    xaxis = columns[3]
    yaxis = columns[0]
    xx = df[xaxis].values
    yy = df[yaxis].values
    dferror = df[columns].copy()
    dferror['ydis'] = yy - np.mean(yy)
    sstot = np.dot(dferror['ydis'],dferror['ydis'])

    X = xx.reshape(-1, 1)
    poly = PolynomialFeatures(order) #order = 0 will result in just an intercept vector
    Xuse = poly.fit_transform(X)    
    
    reg = LinearRegression().fit(Xuse, yy)  
    qm_slopes = reg.coef_
    qm_intercepts = reg.intercept_
    dferror['yhat']= reg.predict(Xuse)
    dferror['yerror'] = dferror['yhat'] - yy
    ssres = np.dot(dferror['yerror'],dferror['yerror'])
    
    nrparams = order + 1

    estimates = {'slopes': qm_slopes, 'intercepts': qm_intercepts, 
                 'ssres': ssres, 'sstot': sstot, 'precision': 1/(ssres/len(yy)), 'dferror': dferror, 'nrparams': nrparams}

    return estimates

def calculate_subrange(df=None, columns=None, order=1):

    xaxis = columns[3]
    yaxis = columns[0]
    dferror = df[columns].copy()

    xx = df[xaxis].values
    yy = df[yaxis].values

    dferror['ydis'] = yy - np.mean(yy)
    sstot = np.dot(dferror['ydis'],dferror['ydis'])

    if order == 0:
        # perform a normal regression
        X = xx.reshape(-1, 1)
        reg = LinearRegression().fit(X, yy)  
        #print(reg.coef_)   
        #print(reg.intercept_)   

        qm_subrange = None
        qm_subrange_se = None 
        qm_slopes = reg.coef_
        qm_intercepts = reg.intercept_
        qm_fitbreaks = None
        qm_betas = None

        dferror['yhat']= reg.predict(X)
        dferror['yerror'] = dferror['yhat'] - yy
        ssres = np.dot(dferror['yerror'],dferror['yerror'])
        nrparams = 2

    else:
        #i = 1
        nrsegments = order+1
        #while i > 0:
        my_pwlf = pwlf.PiecewiseLinFit(xx, yy)
        #res = my_pwlf.fitfast(nrsegments, pop = 10) # 2 line segments, # 2 initializations
        # slower but more likely to reach global optimum, with fitfast the results differ per run
        res = my_pwlf.fit(nrsegments, strategy='best1bin', maxiter=1000, popsize=50, tol=1e-2, mutation=(0.5, 1), recombination=0.7, 
                          seed=None, callback=None, disp=False, polish=True, init='latinhypercube', atol=1e-3) 
        # reduced tol from 1e-3 to 1e-2, reduced atol from 1e-4 to 1e-3
        
        fitbreaks = my_pwlf.fit_breaks

        # our x-axis data is quite discrete, therefore, the algorithm may obtain fit breaks that are the same as the start/end of our data
        # we manually check this, and stop the process if it happens; it is unlikely that an additional break point exists.
        if any(x in fitbreaks[1:-1] for x in [1, 9]):
            #print('yes')
            return calculate_subrange(df=df, columns=columns, order=order-1)

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
        dferror['yhat'] = my_pwlf.predict(xx)
        dferror['yerror'] = dferror['yhat'] - yy
        #print(dferror['yerror'])

        #print('ses linear:', my_pwlf.standard_errors(method='linear'))
        my_pwlf.standard_errors(method='non-linear')
        #print('ses non linear:', errors)
        # not needed since method = non-linear in the my_pwlf package give the same result
        #se, params = my_pwlf.calc_standard_errors_fit_breaks()
        #print('se:' , se)
        #print('params:', params)    
        ses = my_pwlf.se
        #print(ses) # four values... 
        ssres = my_pwlf.ssr
        #print(ssres)
        #print(np.dot(dferror['yerror'],dferror['yerror']))

        qm_subrange = np.round(fitbreaks[1],2) # 1 value
        qm_subrange_se = np.round(ses[3],2) # 1 value

        qm_slopes = np.round(slopes,2) # 2 values
        qm_intercepts = np.round(intercepts,2) # 2 values
        qm_fitbreaks = np.round(fitbreaks,2) # 3 values
        qm_betas = np.round(betas,2) # 3 values
    
        #qm_subrange_ssr = np.round(ssr,2) # 1 value
        #qm_subrange_fit = np.round(np.sum(dferror['yerror']**2)/len(yy),2)

        nrparams = order*2 + 1

    estimates = {'subrange_est': qm_subrange, 'subrange_se': qm_subrange_se, 
                 'slopes': qm_slopes, 'intercepts': qm_intercepts, 'fitbreaks': qm_fitbreaks, 'betas': qm_betas,
                 'ssres': ssres, 'sstot': sstot, 'precision': 1/(ssres/len(yy)), 'dferror': dferror, 'nrparams': nrparams}

    return estimates

def calculate_error_subrange(estimates=None, general_params=None, idxIDs=None):

    # here, we calculate the global error and local error of the subgroup rows 
    dferrorsg = ss.select_subgroup_part_of_target(idxIDs=idxIDs, target=general_params['estimates']['dferror'], case_based_target=False)
    yerrorsg = dferrorsg['yerror'].values
    SSresGlobal = np.dot(yerrorsg,yerrorsg)

    SSresLocal = estimates['ssres']

    return SSresGlobal, SSresLocal

def determine_model_order(df=None, columns=None, startorder=1, maxorder=2):

    #N = len(df[columns[1]].unique()) # number of IDs
    #print(df.head())
    N = len(df) # number of rows # we need this one, because every row is a datapoint in the regression
    #pvalue = 0 # initial  
    go = True
    bic1 = None

    # calculate with order = 0 = linear model
    estimates1 = calculate_subrange(df=df, columns=columns, order=startorder)
    nrparams1 = estimates1['nrparams']
    RSS1 = estimates1['ssres']

    iorder = startorder
    #while ( (pvalue < 0.05) & (iorder < maxorder) ):  
    while ( (go) & (iorder < maxorder) ): 

        iorder += 1    

        # previous model will become lower order model in next iteration
        RSS0 = RSS1.copy()
        nrparams0 = nrparams1
        estimates0 = estimates1.copy()

        # calculate with order = 1 = 1 segment
        estimates1 = calculate_subrange(df=df, columns=columns, order=iorder)
        nrparams1 = estimates1['nrparams']
        RSS1 = estimates1['ssres']

        '''
        # execute f test
        dfn = nrparams1 - nrparams0
        if dfn == 0: 
            RSS0 = RSS1.copy()
            nrparams0 = nrparams1
            estimates0 = estimates1.copy()  
            break

        dfd = N - nrparams1 - 1        
        Fscore = ((RSS0-RSS1)/dfn)/(RSS1/dfd)
        #Fcrit = sc.stats.f.ppf(q=1-0.05, dfn=dfn, dfd=dfd)
        pvalue = 1 - sc.stats.f.cdf(Fscore, dfn=dfn, dfd=dfd)
        '''

        # compare bic, maximize
        #ll0 = (N/2)*np.log(estimates0['precision']) - (N/2)*np.log(2*np.pi) - 0.5*(estimates0['precision'])*RSS0         
        ll0 = -1*N*np.log(RSS0/N)
        #bic0 = ll0-(nrparams0*np.log(N))
        bic0 = ll0-(nrparams0*np.log(N))
        #ll1 = (N/2)*np.log(estimates1['precision']) - (N/2)*np.log(2*np.pi) - 0.5*(estimates1['precision'])*RSS1         
        ll1 = -1*N*np.log(RSS1/N)
        #bic1 = ll1-(nrparams1*np.log(N))
        bic1 = ll1-(nrparams1*np.log(N))
        if bic0 >= bic1:
            go = False        
    
    if iorder == maxorder:
        #if pvalue < 0.05: 
        if go: 
            iorder += 1
            RSS0 = RSS1.copy()
            nrparams0 = nrparams1
            bic0 = bic1
            estimates0 = estimates1.copy()              

    # while loop has stopped
    # use lower order model: continue with RSS0, nrparams0, estimates0
    #print(iorder-1)
    estimates = estimates0.copy()
    estimates.update({'chorder': iorder-1, 'nrparams': nrparams0, 'bic':bic0})

    return estimates

def determine_model_order_reg(df=None, columns=None, startorder=1, maxorder=2):

    N = len(df)
    go = True
    bic1 = None

    # calculate with order = 0
    estimates1 = regression_model(df=df, columns=columns, order=startorder) 
    nrparams1 = estimates1['nrparams']
    RSS1 = estimates1['ssres']

    iorder = startorder
    #while ( (pvalue < 0.05) & (iorder < maxorder) ):  
    while ( (go) & (iorder < maxorder) ): 

        iorder += 1    
        print(iorder)

        # previous model will become lower order model in next iteration
        RSS0 = RSS1.copy()
        nrparams0 = nrparams1
        estimates0 = estimates1.copy()

        # calculate with order = 1 = 1 segment
        estimates1 = regression_model(df=df, columns=columns, order=iorder) 
        nrparams1 = estimates1['nrparams']
        RSS1 = estimates1['ssres']

        # compare bic, maximize
        #ll0 = (N/2)*np.log(estimates0['precision']) - (N/2)*np.log(2*np.pi) - 0.5*(estimates0['precision'])*RSS0         
        ll0 = -1*N*np.log(RSS0/N)
        #bic0 = ll0-(nrparams0*np.log(N))
        bic0 = ll0-(nrparams0*np.log(N))
        #ll1 = (N/2)*np.log(estimates1['precision']) - (N/2)*np.log(2*np.pi) - 0.5*(estimates1['precision'])*RSS1         
        ll1 = -1*N*np.log(RSS1/N)
        #bic1 = ll1-(nrparams1*np.log(N))
        bic1 = ll1-(nrparams1*np.log(N))
        print(bic0)
        print(bic1)
        if bic0 >= bic1:
            go = False        
    
    if iorder == maxorder:
        #if pvalue < 0.05: 
        if go: 
            iorder += 1
            RSS0 = RSS1.copy()
            nrparams0 = nrparams1
            bic0 = bic1
            estimates0 = estimates1.copy()              

    # while loop has stopped
    # use lower order model: continue with RSS0, nrparams0, estimates0
    #print(iorder-1)
    estimates = estimates0.copy()
    estimates.update({'chorder': iorder-1, 'nrparams': nrparams0, 'bic':bic0})

    return estimates


