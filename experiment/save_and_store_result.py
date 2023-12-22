import numpy as np
import pandas as pd
import os

def save_and_store_synthetic_result(syn_simulation_result=None, output_to_path=None):

    distribution_summary = {}
    info_summary_ls = []
    syn_results_ls = []

    for syn in syn_simulation_result:       

        synparams = syn['synparams']
        single_simulation_result = syn['single_simulation_result']
        syn_data_at_path = syn['syn_data_at_path']        
        
        output_to_specific_path = output_to_path + str(list(synparams)) + '/'
        if not os.path.exists(output_to_specific_path):
            os.makedirs(output_to_specific_path)        

        simulation_summary, distribution_summary, info_summary = save_and_store_result(simulation_result=single_simulation_result, output_to_path=output_to_specific_path)
        
        for row in np.arange(0,simulation_summary.shape[0]):
            syn_sum = dict(zip(['N','T','G','SGType'],synparams))
            syn_sum.update(pd.Series.to_dict(simulation_summary.iloc[row,:]))
            syn_results_ls.append(syn_sum)

            an_info_sum = dict(zip(['N','T','G','SGType'],synparams))
            an_info_sum.update(pd.Series.to_dict(info_summary.iloc[row,:]))
            info_summary_ls.append(an_info_sum)

    syn_results = pd.DataFrame.from_records(syn_results_ls)  
    info_results = pd.DataFrame.from_records(info_summary_ls)  
    print(syn_results)  

    return syn_results, distribution_summary, info_results

def save_and_store_result(simulation_result=None, output_to_path=None):

    simulation_summary_ls = []
    distribution_summary_ls = []
    info_summary_ls = []

    for bs in simulation_result:

        params = bs['params']
        result_emm = bs['result_emm']
        general_params = bs['general_params']
        considered_subgroups = bs['considered_subgroups']
        time = bs['time']
        distribution = bs['distribution']    
        attributes = bs['attributes']

        sum = dict(zip(['data','dbs','wcs','dp','md'],params))
        distribution_sum = dict(zip(['data','dbs','wcs','dp','md'],params))
        info_sum = dict(zip(['data','dbs','wcs','dp','md'],params))

        # separately save pd dataframe
        if result_emm is not None:
            store_result_emm = result_emm.drop(['idx_id'],axis=1)
            store_result_emm.to_csv(output_to_path + str(list(params)) + '.txt', sep='\t', index=False)
            sum.update(obtain_summary_values_emm(result_emm=result_emm, general_params=general_params, time=time)) 
            
            info_sum.update(considered_subgroups) 
            info_sum.update(general_params)  
            info_sum.update(attributes)     
            
        if distribution is not None:       
            distribution_params = obtain_summary_values_dfd(distribution=distribution)
            sum.update(distribution_params)
            sum.update(calculate_number_rejected(result_emm=result_emm, distribution_params=distribution_params))
            distribution_sum.update({'distribution':distribution})       
        
        simulation_summary_ls.append(sum)
        distribution_summary_ls.append(distribution_sum)
        info_summary_ls.append(info_sum)

    simulation_summary = pd.DataFrame.from_records(simulation_summary_ls)    
    distribution_summary = pd.DataFrame.from_records(distribution_summary_ls)  
    info_summary = pd.DataFrame.from_records(info_summary_ls)   

    return simulation_summary, distribution_summary, info_summary

def obtain_summary_values_emm(result_emm=None, general_params=None, time=None):

    overall_coverage, cover_counts, expected_cover_count, CR, jsim, jsims = calculate_average_coverage(result_emm=result_emm, general_params=general_params)

    desc_lens, desc_un_lens, nr_unique_atts, attribute_cover_counts, attribute_expected_cover_count, attribute_CR = obtain_description_summary(result_emm=result_emm)

    iqrs = [0.25,0.5,0.75]

    sum_result_emm = {'len_result_set': len(result_emm)}

    iqr_over_names = ['varphi', 'mean_est', 'se_est', 'size_id']
    for name in iqr_over_names:
    
        vals = result_emm[name].quantile(iqrs, interpolation='linear')
        sum_result_emm.update({name+str(int(key*100)):val for key,val in dict(vals).items()})
    
    sum_result_emm.update({
                      'avg_row_size': result_emm['size_rows'].mean(),
                      'expected_cover_count': expected_cover_count
                      })

    vals = np.quantile(list(cover_counts.values()),iqrs)
    sum_result_emm.update(dict(zip(['covercount' + str(int(key*100)) for key in iqrs],vals)))

    sum_result_emm.update({
                      'CR': CR,
                      'overall_coverage': overall_coverage,              

                      'attribute_expected_cover_count': attribute_expected_cover_count,
                      'attribute_CR': attribute_CR
                      })

    vals = np.quantile(desc_lens,iqrs)
    sum_result_emm.update(dict(zip(['desc_len' + str(int(key*100)) for key in iqrs],vals)))
    
    vals = np.quantile(desc_un_lens,iqrs)
    sum_result_emm.update(dict(zip(['desc_un_len' + str(int(key*100)) for key in iqrs],vals)))
                      
    sum_result_emm.update({
                      'nr_unique_atts': nr_unique_atts,
                      'jsim': jsim,
                      'time_minutes': time/60
                      })

    vals = np.quantile(list(jsims.values()),iqrs)
    sum_result_emm.update(dict(zip(['jsim' + str(int(key*100)) for key in iqrs],vals)))

    return sum_result_emm

def calculate_average_coverage(result_emm=None, general_params=None):

    all_ids = general_params['IDs']
    allids_int = general_params['IDs']
    allids_un = []
    for sg in np.arange(0,result_emm.shape[0]):
        ids = result_emm.loc[sg,'idx_id']
        allids_un += ids # store id of all sg in one ls
        allids_int = np.intersect1d(allids_int, ids)
    
    values, counts = np.unique(allids_un, return_counts=True)
    #unids = list(set(allids_un)) # check number of unique id
    
    cover_counts = {id: 0 for id in all_ids}
    cover_counts.update({values[i]:counts[i] for i in range(len(values))})
    expected_cover_count = sum(list(cover_counts.values())) / len(cover_counts.keys())

    overall_coverage = len(values)/len(all_ids)
    CR = sum(np.abs(list(cover_counts.values()) - expected_cover_count)/expected_cover_count) / len(cover_counts.keys())

    # jaccard similarity over all subgroups
    jsim = len(allids_int) / len(values)

    # jaccard similarities for all subgroups
    jsims = {}
    for sg1 in np.arange(0,result_emm.shape[0]):
        for sg2 in np.arange(0,result_emm.shape[0]):
            if sg1 != sg2: 
                ids1 = result_emm.loc[sg1,'idx_id']
                ids2 = result_emm.loc[sg2,'idx_id']
                jsim = len(np.intersect1d(ids1, ids2)) / len(np.unique(ids1 + ids2))
                jsims[(sg1,sg2)] = jsim

    return overall_coverage, cover_counts, expected_cover_count, CR, jsim, jsims

def obtain_description_summary(result_emm=None):

    used_atts = list(result_emm['literal_order'])
    desc_lens = [len(tuple) for tuple in used_atts]
    desc_un_lens = [len(set(tuple)) for tuple in used_atts]

    all_atts = [t for tuple in used_atts for t in tuple]
    nr_unique_atts = len(set(all_atts))

    values, counts = np.unique(all_atts, return_counts=True)
    attribute_cover_counts = {values[i]:counts[i] for i in range(len(values))}
    attribute_expected_cover_count = sum(list(attribute_cover_counts.values())) / len(attribute_cover_counts.keys())

    attribute_CR = sum(np.abs(list(attribute_cover_counts.values()) - attribute_expected_cover_count)/attribute_expected_cover_count) / len(attribute_cover_counts.keys())

    return desc_lens, desc_un_lens, nr_unique_atts, attribute_cover_counts, attribute_expected_cover_count, attribute_CR

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





