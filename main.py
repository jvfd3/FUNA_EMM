import numpy as np
import pandas as pd
import os

import experiment.analysis as an
import experiment.save_and_store_result as ssr

def main(data_name=None, data_from=None, datasets_names=None, simulation_params=None, synthetic_params=None,
         beam_search_params=None, model_params=None, alg_constraints=None, wcs_params=None, dfd_params=None, date=None, output_to=None):

    # save result at
    output_to_mypath = output_to + data_name + '/' + str(date) + '/' 
    if not os.path.exists(output_to_mypath):
        os.makedirs(output_to_mypath)

    if synthetic_params is None: 
        # simulation_result is a list of dictionaries
        simulation_result = an.analysis(data_name=data_name, data_from=data_from, datasets_names=datasets_names, simulation_params=simulation_params, beam_search_params=beam_search_params, model_params=model_params, alg_constraints=alg_constraints, dfd_params=dfd_params, wcs_params=wcs_params)
        simulation_summary, distribution_summary, info_summary = ssr.save_and_store_result(simulation_result=simulation_result, output_to_mypath=output_to_mypath)
    
    elif synthetic_params is not None:
        syn_simulation_result = an.synthetic_analysis(datasets_names=datasets_names, synthetic_params=synthetic_params, simulation_params=simulation_params, beam_search_params=beam_search_params, model_params=model_params, alg_constraints=alg_constraints, dfd_params=dfd_params, wcs_params=wcs_params)
        simulation_summary, distribution_summary, info_summary = ssr.save_and_store_synthetic_result(syn_simulation_result=syn_simulation_result)

    # save summary        
    beam_search_params.update(simulation_params)
    beam_search_params.update(dfd_params)
    beam_search_params.update(alg_constraints)
    beam_search_params.update(wcs_params)
    
    dfs = {'simulation_summary': simulation_summary, 'distributions': distribution_summary, 'analysis_info': info_summary, 'experiment_info': pd.DataFrame(dict([(k,pd.Series(v)) for k,v in beam_search_params.items()]))}
    excel_file_name = output_to_mypath + str(list(simulation_params.values())) + '_' + '.xlsx'
    
    writer = pd.ExcelWriter(excel_file_name, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()    

if __name__ == '__main__':

    '''
    # FUNA
    main(data_name='FUNA', 
         #datasets_names=['desc_target','desc','long_target','long','wide_target','wide','wide_10','wide_50','wide_90'],
         #datasets_names=['desc_target', 'long_target','wide_target'],
         datasets_names=['long_target'],
         #simulation_params = {'wcs': [True, False], 'dbs': [True, False], 'dp': [True, False], 'md': ['without','separate','included','knn']},
         simulation_params = {'dbs': [True, False], 'wcs': [True, False], 'dp': [True, False], 'md': ['without'], 'sample': True}, 
         # sample = True means that we use 5\% of cases and NC columns (+ language, sex, grade) only, retrieve_data.py
         synthetic_params = None,
         beam_search_params = {'b': 8, 'w': 10, 'd': 5, 'q': 10}, # for now, we use a simple target model
         model_params = {'model': 'zmean'},
         alg_constraints = {'min_size': 0.05},
         dfd_params = {'make_normal': True, 'make_dfd': True, 'm': 2},
         wcs_params = {'gamma': 0.6},
         date='15122023', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''

    # Synthetic
    main(data_name='synthetic', 
         datasets_names=['desc_target', 'long_target','wide_target'],
         simulation_params = {'dbs': [False], 'wcs': [False], 'dp': [False], 'md': ['without'], 'sample': None},
         synthetic_params = {'N': [10, 100], 'T': [5], 'G': [5]},
         beam_search_params = {'b': 8, 'w': 10, 'd': 3, 'q': 10}, # for now, we use a simple target model
         model_params = {'model': 'zmean'},
         alg_constraints = {'min_size': 0.05},
         dfd_params = {'make_normal': True, 'make_dfd': False, 'm': None},
         wcs_params = {'gamma': None},
         date='15122023', 
         data_from="./input/",
         output_to="./output/")
