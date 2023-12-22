import pandas as pd
import numpy as np   

def create_extra_descriptors(dflong=None, synparams=None, info=None):

    N = synparams[0]
    T = synparams[1]

    nrinvar = 5
    nrvar = 5

    dfextra = dflong.copy()
    
    # 5 time variant descriptors
    for cov in np.arange(1,nrvar+1):
        dfextra['binvar' + str(cov)] = np.random.binomial(n=1, p=0.5, size=N*T)

    # 5 time invariant descriptors
    for cov in np.arange(1,nrinvar+1):
        dfextra['bininvar' + str(cov)] = np.repeat(np.random.binomial(n=1, p=0.5, size=N),T)

    info['extra_desc_invar'] = ['bininvar'+str(i) for i in np.arange(1,nrinvar+1)]
    info['extra_desc_var'] = ['binvar'+str(i) for i in np.arange(1,nrvar+1)]

    return dfextra, info