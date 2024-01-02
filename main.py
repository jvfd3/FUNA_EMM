import numpy as np
import pandas as pd
import os

import experiment.analysis as an
import experiment.save_and_store_result as ssr

def main(data_name=None, data_from=None, datasets_names=None, simulation_params=None, synthetic_params=None,
         beam_search_params=None, model_params=None, alg_constraints=None, wcs_params=None, dfd_params=None, date=None, output_to=None):

    # create path and empty output file 
    output_to_path = output_to + data_name + '/' + 'date' + str(date) + '/'
    if not os.path.exists(output_to_path):
        os.makedirs(output_to_path)    
    excel_file_name, sheet_names = ssr.create_empty_output_file(output_to_path=output_to_path)

    if synthetic_params is None: 
        an.analysis(data_name=data_name, data_from=data_from, datasets_names=datasets_names, simulation_params=simulation_params, 
                    beam_search_params=beam_search_params, model_params=model_params, alg_constraints=alg_constraints, 
                    dfd_params=dfd_params, wcs_params=wcs_params, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)
    
    elif synthetic_params is not None:
        an.synthetic_analysis(datasets_names=datasets_names, synthetic_params=synthetic_params, data_from=data_from, simulation_params=simulation_params, 
                              beam_search_params=beam_search_params, model_params=model_params, alg_constraints=alg_constraints, dfd_params=dfd_params, wcs_params=wcs_params,
                              output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    # final update with experiment info                        
    experiment_info = {**beam_search_params, **simulation_params, **synthetic_params, **dfd_params, **alg_constraints, **wcs_params}
    ssr.final_update_experiment_info(excel_file_name=excel_file_name, experiment_info=experiment_info, sheet_names=sheet_names)


if __name__ == '__main__':

    # FUNA
    '''
    main(data_name='FUNA', 
         #datasets_names=['desc_target','desc','long_target','long','wide_target','wide','wide_10','wide_50','wide_90'],
         #datasets_names=['desc_target', 'long_target','wide_target'],
         datasets_names=['long_target'],
         #simulation_params = {'wcs': [True, False], 'dbs': [True, False], 'dp': [True, False], 'md': ['without','separate','included','knn']},
         simulation_params = {'dbs': [True, False], 'wcs': [True, False], 'dp': [True, False], 'md': ['without'], 'sample': True}, 
         # sample = True means that we use 5\% of cases and NC columns (+ language, sex, grade) only, retrieve_data.py
         synthetic_params = None,
         beam_search_params = {'b': 8, 'w': 10, 'd': 5, 'q': 10}, # for now, we use a simple target model
         model_params = {'model': 'zmean', 'column_name': 'DMTime'},
         alg_constraints = {'min_size': 0.05},
         dfd_params = {'make_normal': True, 'make_dfd': True, 'm': 2},
         wcs_params = {'gamma': 0.6},
         date='15122023', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''

    # Synthetic
    main(data_name='synthetic', 
         datasets_names=['long_target'],
         simulation_params = {'dbs': [False], 'wcs': [False], 'dp': [False], 'md': ['without'], 'target_model': ['zmean_high'], 'sample': None},
         synthetic_params = {'N': [10], 'T': [3], 'G': [2], 'SGTypes': ['C'], 'minsize': ['default'], 'noise': [0.1]},
         beam_search_params = {'b': 2, 'w': 5, 'd': 2, 'q': 5}, 
         model_params = {'model': None, 'column_name': 'Target'}, #zmean, zmean_high, zslope_high
         alg_constraints = {'min_size': None}, # adapt to G^T
         dfd_params = {'make_normal': True, 'make_dfd': False, 'm': None},
         wcs_params = {'gamma': 0.9},
         date='02012024', 
         data_from="./data_input/",
         output_to="./output/"
    )
