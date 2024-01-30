import numpy as np
import pandas as pd
import itertools as it
import math

def obtain_summary_values_emm(result_emm=None, general_params=None, time=None, sel_params=None, attributes=None):

    iqrs = [0.25,0.5,0.75]

    sum_result_emm = {'len_result_set': len(result_emm)}

    iqr_over_names = ['varphi', 'size_id', 'size_rows', 'mean_est', 'mean_se', 'slope_est', 'slope_se', 'subrange_est', 'subrange_se']
    for name in iqr_over_names:
        if name in result_emm.columns.values: 
            vals = result_emm[name].quantile(iqrs, interpolation='linear')
            sum_result_emm.update({name+str(int(key*100)):np.round(val,2) for key,val in dict(vals).items()})
    
    # redundancy metrics
    cover_counts, expected_cover_count, CR, jentropy, jsims = calculate_average_coverage(result_emm=result_emm, general_params=general_params, sel_params=sel_params)

    sum_result_emm.update({
                      #'avg_row_size': result_emm['size_rows'].mean(),
                      'expected_cover_count': expected_cover_count
                      })

    vals = np.quantile(list(cover_counts.values()),iqrs)
    sum_result_emm.update(dict(zip(['covercount' + str(int(key*100)) for key in iqrs],vals)))

    sum_result_emm.update({
                      'CR': CR,
                      'jentropy': jentropy,         
                      })

    vals = np.quantile(list(jsims.values()),iqrs)
    sum_result_emm.update(dict(zip(['jsim' + str(int(key*100)) for key in iqrs],vals)))

    # description metrics
    desc_lens, desc_un_lens, nr_unique_atts, attribute_cover_counts, attribute_expected_cover_count, attribute_CR = calculate_description_summary(result_emm=result_emm, attributes=attributes)

    vals = np.quantile(desc_lens,iqrs)
    sum_result_emm.update(dict(zip(['desc_len' + str(int(key*100)) for key in iqrs],vals)))
    
    vals = np.quantile(desc_un_lens,iqrs)
    sum_result_emm.update(dict(zip(['desc_un_len' + str(int(key*100)) for key in iqrs],vals)))
                      
    sum_result_emm.update({
                      'attribute_expected_cover_count': attribute_expected_cover_count,
                      'attribute_CR': attribute_CR
                      'nr_unique_atts': nr_unique_atts
                      })

    # other
    sum_result_emm.update({'time_minutes': time/60})    

    return sum_result_emm

def calculate_description_summary(result_emm=None, attributes=None):

    all_ats = attributes['bin_atts'] + attributes['nom_atts'] + attributes['num_atts'] + attributes['ord_atts']
    attribute_cover_counts = {att: 0 for att in all_ats}

    used_atts = list(result_emm['literal_order'])
    desc_lens = [len(tuple) for tuple in used_atts]
    desc_un_lens = [len(set(tuple)) for tuple in used_atts]

    all_used_atts = [t for tuple in used_atts for t in tuple]
    nr_unique_atts = len(set(all_used_atts))       

    #values, counts = np.unique(all_used_atts, return_counts=True)
    #attribute_cover_counts.update({values[i]:counts[i] for i in range(len(values))})
    attribute_cover_counts = dict((x,all_used_atts.count(x)) for x in set(all_ats))    
    attribute_expected_cover_count = sum(list(attribute_cover_counts.values())) / len(attribute_cover_counts.keys())

    attribute_CR = sum([(np.abs(x-attribute_expected_cover_count)/attribute_expected_cover_count) for x in list(attribute_cover_counts.values())]) / len(attribute_cover_counts.keys()) 

    return desc_lens, desc_un_lens, nr_unique_atts, attribute_cover_counts, attribute_expected_cover_count, attribute_CR

def calculate_average_coverage(result_emm=None, general_params=None, sel_params=None):
    
    # these values are calculated for rows or ids depending on data format (given in params[0])
    cover_counts, expected_cover_count, CR = calculate_cr(result_emm=result_emm, general_params=general_params, sel_params=sel_params)
    jentropy = calculate_jentropy(result_emm=result_emm, general_params=general_params, sel_params=sel_params)
    jsims = calculate_jsim(result_emm=result_emm, sel_params=sel_params)

    return cover_counts, expected_cover_count, CR, jentropy, jsims

def calculate_cr(result_emm=None, general_params=None, sel_params=None):

    # for long format: per row
    if "long" in sel_params['data_key']:
        all_rows = list(np.arange(0, general_params['nrrows']))
        allrows_int = list(np.arange(0, general_params['nrrows']))
        allrows_un = []
        for sg in np.arange(0,result_emm.shape[0]):
            idx_sg = result_emm.loc[sg,'idx_sg']
            allrows_un += idx_sg
            allrows_int = np.intersect1d(allrows_int, idx_sg)   
        #values, counts = np.unique(allrows_un, return_counts=True)
        #cover_counts = {row: 0 for row in all_rows}
        cover_counts = dict((x,allrows_un.count(x)) for x in set(all_rows))
    # for wide and desc format: per ID
    else: 
        allids_int = general_params['IDs'].copy()
        all_ids = general_params['IDs'].copy()
        allids_un = []
        for sg in np.arange(0,result_emm.shape[0]):
            ids = result_emm.loc[sg,'idx_id']
            allids_un += ids # store id of all sg in one ls
            allids_int = np.intersect1d(allids_int, ids)
        #values, counts = np.unique(allids_un, return_counts=True)
        #cover_counts = {id: 0 for id in all_ids}
        cover_counts = dict((x,allids_un.count(x)) for x in set(all_ids))

    #cover_counts.update({values[i]:counts[i] for i in range(len(values))})
    expected_cover_count = sum(list(cover_counts.values())) / len(cover_counts.keys())
    CR = sum([(np.abs(x-expected_cover_count)/expected_cover_count) for x in list(cover_counts.values())]) / len(cover_counts.keys())    

    return cover_counts, expected_cover_count, CR

def calculate_jentropy(result_emm=None, general_params=None, sel_params=None):

    k = result_emm.shape[0]
    combs = list(it.product([0,1],repeat=k))
    res = {}

    # for long format: per row
    if "long" in sel_params['data_key']:
        NT = general_params['nrrows']
        for comb in combs:
            idx1 = list(np.arange(0, general_params['nrrows']))
            idx0 = []
            for count, b in enumerate(comb):
                idx_sg = result_emm.loc[count,'idx_sg']
                if b == 1:
                    idx1 = np.intersect1d(idx1, idx_sg)
                if b == 0:
                    idx0 += idx_sg
            idxlist = np.setdiff1d(idx1,idx0)
            prop = len(idxlist)/NT
            if prop == 0.0:
                prop = np.nan
            res.update({comb: prop})

    # for wide and desc format: per ID
    else: 
        N = len(general_params['IDs'])
        for comb in combs:
            ids1 = general_params['IDs'].copy()
            ids0 = []
            for count, b in enumerate(comb):
                ids = result_emm.loc[count,'idx_id']
                if b == 1:
                    ids1 = np.intersect1d(ids1, ids)
                if b == 0:
                    ids0 += ids
            idlist = np.setdiff1d(ids1,ids0) # the ones in ids1 that are not in ids0
            prop = len(idlist)/N
            if prop == 0.0: # RS should check whether it is correct that prop can be 0.0
                prop = np.nan
            #print(comb, ':', prop)
            res.update({comb: prop}) # proportion
    
    vals = list(res.values())
    logvals = [math.log(i,2) for i in vals]
    # replace np.nan with 0, if fraction approaches 0, the entropy is 0
    entropy = [a*b for a,b in zip(np.nan_to_num(vals),np.nan_to_num(logvals))]
    jentropy = -1 * sum(entropy)

    return jentropy

def calculate_jsim(result_emm=None, sel_params=None):

    # jaccard similarities for all subgroups
    jsims = {}
    
    # for long format: per row
    if "long" in sel_params['data_key']:
        for sg1 in np.arange(0,result_emm.shape[0]):
            for sg2 in np.arange(0,result_emm.shape[0]):
                if sg1 < sg2: # only one triangular is needed
                    idx1 = result_emm.loc[sg1,'idx_sg']
                    idx2 = result_emm.loc[sg2,'idx_sg']
                    jsim = len(np.intersect1d(idx1, idx2)) / len(np.unique(idx1 + idx2))
                    jsims[(sg1,sg2)] = jsim

    # for wide and desc format: per ID
    else:     
        for sg1 in np.arange(0,result_emm.shape[0]):
            for sg2 in np.arange(0,result_emm.shape[0]):
                if sg1 < sg2: # only one triangular is needed
                    ids1 = result_emm.loc[sg1,'idx_id']
                    ids2 = result_emm.loc[sg2,'idx_id']
                    jsim = len(np.intersect1d(ids1, ids2)) / len(np.unique(ids1 + ids2))
                    jsims[(sg1,sg2)] = jsim

    return jsims

def obtain_summary_values_dfd(distribution=None):

    m = len(distribution)
    mu = np.mean(distribution)
    std = np.std(distribution)

    cutoff90 = mu + 1.645*std
    cutoff95 = mu + 1.96*std
    cutoff99 = mu + 2.58*std

    distribution_params = {'m': m, 'mu': mu, 'std': std, 
                           'cutoff90': cutoff90, 'cutoff95': cutoff95, 'cutoff99': cutoff99}   
    
    return distribution_params

def calculate_number_rejected(result_emm=None, distribution_params=None):

    # check how many subgroups will be rejected
    rej90 = sum(result_emm['varphi'] < distribution_params['cutoff90'])
    rej95 = sum(result_emm['varphi'] < distribution_params['cutoff95'])
    rej99 = sum(result_emm['varphi'] < distribution_params['cutoff99'])
                
    rej_subgroups = {'rej90': rej90, 'rej95': rej95, 'rej99': rej99}        

    return rej_subgroups