import numpy as np
import pandas as pd

def save_and_store_result(simulation_result=None, output_to_mypath=None):

    simulation_summary_ls = []
    distribution_summary_ls = []
    for bs in simulation_result:

        params = bs['params']
        result_emm = bs['result_emm']
        general_params = bs['general_params']
        considered_subgroups = bs['considered_subgroups']
        time = bs['time']
        distribution = bs['distribution']    

        sum = dict(zip(['data','wcs','dbs','dp','md'],params))
        distribution_sum = dict(zip(['data','wcs','dbs','dp','md'],params))

        # separately save pd dataframe
        if result_emm is not None:
            store_result_emm = result_emm.drop(['idx_id'],axis=1)
            store_result_emm.to_csv(output_to_mypath + str(params) + '.txt', sep='\t', index=False)
            sum.update(obtain_summary_values_emm(result_emm=result_emm, general_params=general_params, time=time)) 
            sum.update(considered_subgroups)

        if distribution is not None:       
            distribution_params = obtain_summary_values_dfd(distribution=distribution, result_emm=result_emm)
            sum.update(distribution_params)
            sum.update(calculate_number_rejected(result_emm=result_emm, distribution_params=distribution_params))
            distribution_sum.update({'distribution':distribution})

        simulation_summary_ls.append(sum)
        distribution_summary_ls.append(distribution_sum)

    simulation_summary = pd.DataFrame.from_records(simulation_summary_ls)    
    distribution_summary = pd.DataFrame.from_records(distribution_summary_ls)    

    return simulation_summary, distribution_summary

def obtain_summary_values_emm(result_emm=None, general_params=None, time=None):

    overall_coverage, cover_counts, expected_cover_count, CR, jsim, jsims = calculate_average_coverage(result_emm=result_emm, general_params=general_params)

    tuple_lens, nr_unique_atts, attribute_cover_counts, attribute_expected_cover_count, attribute_CR = obtain_description_summary(result_emm=result_emm)

    sum_result_emm = {'avg_varphi': result_emm['varphi'].mean(),
                      'median_varphi': result_emm['varphi'].median(),
                      'max_varphi': result_emm['varphi'].max(),
                      'min_varphi': result_emm['varphi'].min(),

                      'avg_mean': result_emm['mean_est'].mean(),
                      'max_mean': result_emm['mean_est'].max(),
                      'min_mean': result_emm['mean_est'].min(),
                      'avg_mean_se': result_emm['se_est'].mean(),
                      'max_mean_se': result_emm['se_est'].max(),
                      'min_mean_se': result_emm['se_est'].min(),

                      'avg_sg_size': result_emm['size_id'].mean(),
                      'median_sg_size': result_emm['size_id'].median(),
                      'max_sg_size': result_emm['size_id'].max(),
                      'min_sg_size': result_emm['size_id'].min(),
                      'avg_row_size': result_emm['size_rows'].mean(),

                      'expected_cover_count': expected_cover_count,
                      'median_cover_count': np.median(list(cover_counts.values())),
                      'std_cover_count': np.std(list(cover_counts.values())),
                      'min_count': np.min(list(cover_counts.values())),
                      'max_cover_count': np.max(list(cover_counts.values())),

                      'overall_coverage': overall_coverage,
                      'CR': CR,
                      'attribute_CR': attribute_CR,

                      'attribute_expected_cover_count': attribute_expected_cover_count,
                      'avg_tuple_lens': np.mean(tuple_lens),
                      'median_tuple_lens': np.median(tuple_lens),
                      'max_tuple_lens': np.max(tuple_lens),
                      'min_tuple_lens': np.min(tuple_lens),
                      'nr_unique_atts': nr_unique_atts,

                      'jsim': jsim,
                      'avg': np.mean(list(jsims.values())),
                      'median_jsim': np.median(list(jsims.values())),
                      'max_jsim': np.max(list(jsims.values())),
                      'min_jsim': np.min(list(jsims.values())),

                      'time_minutes': time/60}

    return sum_result_emm

def calculate_average_coverage(result_emm=None, general_params=None):

    allids = general_params['IDs']
    allids_un = []
    for sg in np.arange(0,result_emm.shape[0]):
        ids = result_emm.loc[sg,'idx_id']
        allids_un += ids # store id of all sg in one ls
        allids = np.intersect1d(allids, ids)
    
    values, counts = np.unique(allids_un, return_counts=True)
    #unids = list(set(allids_un)) # check number of unique id
    
    cover_counts = {id: 0 for id in allids}
    cover_counts.update({values[i]:counts[i] for i in range(len(values))})
    expected_cover_count = sum(list(cover_counts.values())) / len(cover_counts.keys())

    overall_coverage = len(values)/len(general_params['IDs'])
    CR = sum(np.abs(list(cover_counts.values()) - expected_cover_count)/expected_cover_count) / len(cover_counts.keys())

    # jaccard similarity over all subgroups
    jsim = len(allids) / len(values)

    # jaccard similarities for all subgroups
    jsims = {}
    for sg1 in np.arange(0,result_emm.shape[0]):
        for sg2 in np.arange(0,result_emm.shape[0]):
            ids1 = result_emm.loc[sg1,'idx_id']
            ids2 = result_emm.loc[sg2,'idx_id']
            jsim = len(np.intersect1d(ids1, ids2)) / len(np.unique(ids1 + ids2))
            jsims[(sg1,sg2)] = jsim

    return overall_coverage, cover_counts, expected_cover_count, CR, jsim, jsims

def obtain_description_summary(result_emm=None):

    used_atts = list(result_emm['literal_order'])
    tuple_lens = [len(tuple) for tuple in used_atts]

    all_atts = [t for tuple in used_atts for t in tuple]
    nr_unique_atts = len(set(all_atts))

    values, counts = np.unique(all_atts, return_counts=True)
    attribute_cover_counts = {values[i]:counts[i] for i in range(len(values))}
    attribute_expected_cover_count = sum(list(attribute_cover_counts.values())) / len(attribute_cover_counts.keys())

    attribute_CR = sum(np.abs(list(attribute_cover_counts.values()) - attribute_expected_cover_count)/attribute_expected_cover_count) / len(attribute_cover_counts.keys())

    return tuple_lens, nr_unique_atts, attribute_cover_counts, attribute_expected_cover_count, attribute_CR

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





