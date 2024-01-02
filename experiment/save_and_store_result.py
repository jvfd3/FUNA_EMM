import numpy as np
import pandas as pd
import itertools as it
import os

def create_empty_output_file(output_to_path=None):

    dfs = {'simulation_summary': pd.DataFrame(), 'distributions': pd.DataFrame(), 
           'analysis_info': pd.DataFrame(), 'experiment_info': pd.DataFrame()}
    excel_file_name = output_to_path + 'output.xlsx'

    write_to_file(excel_file_name=excel_file_name, dfs=dfs)
    
    sheet_names = dfs.keys()

    return excel_file_name, sheet_names

def update_output_file(excel_file_name=None, sheet_names=None, result_sum=None, distribution_sum=None, info_sum=None):     

    # open output file at location excel_file_name
    dfs = open_file(excel_file_name=excel_file_name, sheet_names=sheet_names)

    if result_sum is not None:
        df = dfs['simulation_summary']
        dfnew = pd.concat((df, pd.DataFrame(result_sum,index=[0])))
        dfs['simulation_summary'] = dfnew
    
    if distribution_sum is not None:
        df = dfs['distributions']
        dfnew = pd.concat((df, pd.DataFrame(distribution_sum,index=[0])))
        dfs['distributions'] = dfnew

    if info_sum is not None:
        df = dfs['analysis_info']
        dfnew = pd.concat((df, pd.DataFrame(pd.Series(info_sum))),axis=1)
        dfs['analysis_info'] = dfnew

    write_to_file(excel_file_name=excel_file_name, dfs=dfs)

    return True

def update_info_about_synthetic_result(synparamset=None, SGTypes=None, excel_file_name=None, sheet_names=None):

    dfs = open_file(excel_file_name=excel_file_name, sheet_names=sheet_names)
    nrows = dfs['simulation_summary'].shape[0]
    
    # create colums and rows
    combs = [(*x, y) for x, y in list(it.product(synparamset, SGTypes))]
    df = pd.DataFrame(combs, columns=['N', 'T', 'G', 'minsize', 'noise', 'SGType'])
    nrrepeat = nrows / df.shape[0]

    dfcombs = pd.DataFrame(np.repeat(df.values, nrrepeat, axis=0))
    dfcombs.columns = df.columns
    
    simsum = dfs['simulation_summary']
    dfnew = pd.concat((dfcombs, simsum), axis=1)
    dfs['simulation_summary'] = dfnew

    write_to_file(excel_file_name=excel_file_name, dfs=dfs)

    return True

def final_update_experiment_info(excel_file_name=None, experiment_info=None, sheet_names=None):

    dfs = open_file(excel_file_name=excel_file_name, sheet_names=sheet_names)
    dfs['experiment_info'] = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in experiment_info.items()]))
    dfs['analysis_info'] = dfs['analysis_info'].T

    print(dfs['simulation_summary'])
    
    write_to_file(excel_file_name=excel_file_name, dfs=dfs)

    return True

def open_file(excel_file_name=None, sheet_names=None):

    dfs = {}
    for sheet_name in sheet_names:
        dfs[sheet_name] = pd.read_excel(excel_file_name, sheet_name=sheet_name)

    return dfs

def write_to_file(excel_file_name=None, dfs=None):

    writer = pd.ExcelWriter(excel_file_name, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()    

    return True

def save_and_store_result(simulation_result=None, output_to_path=None, excel_file_name=None, sheet_names=None):

    params = simulation_result['params']
    result_emm = simulation_result['result_emm']
    general_params = simulation_result['general_params']
    considered_subgroups = simulation_result['considered_subgroups']
    time = simulation_result['time']
    distribution = simulation_result['distribution']    
    attributes = simulation_result['attributes']

    result_sum = dict(zip(['data','dbs','wcs','dp','md','tm'],params))
    distribution_sum = dict(zip(['data','dbs','wcs','dp','md', 'tm'],params))
    info_sum = dict(zip(['data','dbs','wcs','dp','md', 'tm'],params))

    # separately save pd dataframe with results list of one beam search
    if result_emm is not None:
        store_result_emm = result_emm.drop(['idx_id'],axis=1)
        store_result_emm.to_csv(output_to_path + str(list(params)) + '.txt', sep='\t', index=False)
        result_sum.update(obtain_summary_values_emm(result_emm=result_emm, general_params=general_params, time=time)) 
            
        info_sum.update(considered_subgroups) 
        info_sum.update(general_params)  
        info_sum.update(attributes)     
            
    if distribution is not None:       
        distribution_params = obtain_summary_values_dfd(distribution=distribution)
        sum.update(distribution_params)
        sum.update(calculate_number_rejected(result_emm=result_emm, distribution_params=distribution_params))
        distribution_sum.update({'distribution':distribution})  

    # open empty excel file and add simulation summary, distribution summary and info summary
    update_output_file(excel_file_name=excel_file_name, result_sum=result_sum, distribution_sum=distribution_sum, info_sum=info_sum, sheet_names=sheet_names)     
        
    #simulation_summary_ls.append(sum)
    #distribution_summary_ls.append(distribution_sum)
    #info_summary_ls.append(info_sum)

    #simulation_summary = pd.DataFrame.from_records(simulation_summary_ls)    
    #distribution_summary = pd.DataFrame.from_records(distribution_summary_ls)  
    #info_summary = pd.DataFrame.from_records(info_summary_ls)  
    
    return True

def obtain_summary_values_emm(result_emm=None, general_params=None, time=None):

    overall_coverage, cover_counts, expected_cover_count, CR, jsim, jsims = calculate_average_coverage(result_emm=result_emm, general_params=general_params)

    desc_lens, desc_un_lens, nr_unique_atts, attribute_cover_counts, attribute_expected_cover_count, attribute_CR = obtain_description_summary(result_emm=result_emm)

    iqrs = [0.25,0.5,0.75]

    sum_result_emm = {'len_result_set': len(result_emm)}

    iqr_over_names = ['varphi', 'mean_est', 'se_est', 'slope_est', 'se_slope', 'size_id']
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





