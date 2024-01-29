import numpy as np
import pandas as pd
import itertools as it
import os
import math

import experiment.process_result as prr

def create_empty_output_file(output_to_path=None):

    dfs = {'simulation_summary': pd.DataFrame(), 'analysis_info': pd.DataFrame()}
    excel_file_name = output_to_path + 'output.xlsx'

    write_to_file(excel_file_name=excel_file_name, dfs=dfs)
    
    sheet_names = dfs.keys()

    return excel_file_name, sheet_names

def update_output_file(excel_file_name=None, sheet_names=None, result_sum=None, info_sum=None):     

    # open output file at location excel_file_name
    dfs = open_file(excel_file_name=excel_file_name, sheet_names=sheet_names)

    if result_sum is not None:
        df = dfs['simulation_summary']
        dfnew = pd.concat((df, pd.DataFrame(result_sum,index=[0])))
        dfs['simulation_summary'] = dfnew
    
    '''
    if distribution_sum is not None:
        df = dfs['distributions']
        dfnew = pd.concat((df, pd.Series(distribution_sum).to_frame().reset_index(drop=True)),axis=1,ignore_index=True)
        dfs['distributions'] = dfnew
    '''

    if info_sum is not None:
        df = dfs['analysis_info']
        dfnew = pd.concat((df, pd.Series(info_sum).to_frame().reset_index(drop=True)),axis=1,ignore_index=True)
        dfs['analysis_info'] = dfnew

    write_to_file(excel_file_name=excel_file_name, dfs=dfs)

    return True

def update_info_about_synthetic_result(synparamset=None, SGTypes=None, excel_file_name=None, sheet_names=None):

    dfs = open_file(excel_file_name=excel_file_name, sheet_names=sheet_names)
    nrows = dfs['simulation_summary'].shape[0]
    
    # create colums and rows
    combs = [(*x, y) for x, y in list(it.product(synparamset, SGTypes))]
    df = pd.DataFrame(combs, columns=['N', 'T', 'G', 'noise', 'SGType'])
    nrrepeat = nrows / df.shape[0]

    dfcombs = pd.DataFrame(np.repeat(df.values, nrrepeat, axis=0))
    dfcombs.columns = df.columns
    
    simsum = dfs['simulation_summary']
    dfnew = pd.concat((dfcombs, simsum), axis=1)
    dfs['simulation_summary'] = dfnew

    write_to_file(excel_file_name=excel_file_name, dfs=dfs)

    return True

def final_update_result(excel_file_name=None, sheet_names=None):

    dfs = open_file(excel_file_name=excel_file_name, sheet_names=sheet_names)
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

    sel_params = simulation_result['params'] # dictionary
    result_emm = simulation_result['result_emm'] # pd with uneven columns
    general_params = simulation_result['general_params']
    considered_subgroups = simulation_result['considered_subgroups']
    time = simulation_result['time']
    distribution = simulation_result['distribution']    
    attributes = simulation_result['attributes']

    result_sum = sel_params.copy()
    info_sum = sel_params.copy()

    # separately save pd dataframe with results list of one beam search
    if result_emm is not None:
        store_result_emm = result_emm.drop(['idx_id', 'idx_sg'],axis=1)
        store_result_emm.to_csv(output_to_path + str(list(sel_params.values())) + '.txt', sep='\t', index=False)
        result_sum.update(prr.obtain_summary_values_emm(result_emm=result_emm, general_params=general_params, time=time, sel_params=sel_params, attributes=attributes)) 
            
        info_sum.update(considered_subgroups) 
        info_sum.update(general_params)  
        info_sum.update(attributes)     
            
    if distribution is not None:     
        distribution_params = prr.obtain_summary_values_dfd(distribution=distribution)
        result_sum.update(distribution_params)
        result_sum.update(prr.calculate_number_rejected(result_emm=result_emm, distribution_params=distribution_params))
        info_sum.update({'distribution':distribution})  

    # open empty excel file and add simulation summary, distribution summary and info summary
    update_output_file(excel_file_name=excel_file_name, result_sum=result_sum, info_sum=info_sum, sheet_names=sheet_names)     
    
    return True





