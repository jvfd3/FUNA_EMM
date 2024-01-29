import numpy as np
import pandas as pd
import os

import experiment.analysis as an
import experiment.save_and_store_result as ssr

def main(data_name=None, data_from=None, datasets_names=None, synthetic_params=None, sim_params=None, extra_info=None, date=None, output_to=None):

    # create path and empty output file 
    output_to_path = output_to + data_name + '/' + 'date' + str(date) + '/'
    if not os.path.exists(output_to_path):
        os.makedirs(output_to_path)    
    excel_file_name, sheet_names = ssr.create_empty_output_file(output_to_path=output_to_path)

    if synthetic_params is None: 
        an.analysis(data_name=data_name, data_from=data_from, datasets_names=datasets_names, sim_params=sim_params,
                    extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)
    
    elif synthetic_params is not None:
        an.synthetic_analysis(datasets_names=datasets_names, synthetic_params=synthetic_params, data_from=data_from, sim_params=sim_params, 
                              extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    ssr.final_update_result(excel_file_name=excel_file_name, sheet_names=sheet_names)

if __name__ == '__main__':

    '''   
    # Synthetic
    main(data_name='synthetic', 
         datasets_names=['long_target_without', 'long_target_with', 'wide_target', 'desc_target_perfect', 'desc_target_medium'], 
         #datasets_names=['desc_target_perfect'], 
         synthetic_params = {'N': [10000], 'T': [10], 'G': [3], 'noise': [0.1], 'SGTypes': ['D','E']},
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['zmean_high', 'zslope_high'],
                       'dbs': [False], 'wcs': [False], 'gamma': [None], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]},           
         extra_info = {'target_column_names': ['Target','IDCode','TimeInd'], 'sample': None, 'run_beam_search': True, 'make_dfd': True, 'm': 5},
         date='24012024', 
         data_from="./data_input/",
         output_to="./output/")
    
    # FUNA    
    main(data_name='FUNA', 
         datasets_names=['desc_target','desc','long_target','long','wide_target','wide','wide_10','wide_50','wide_90'],
         #datasets_names=['desc_target', 'long_target','wide_target'],
         #datasets_names=['desc_target'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['zmean_high'],
                       'dbs': [True], 'wcs': [True], 'gamma': [0.9], 'dp': [True], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd'], 'sample': True, 'run_beam_search': True, 'make_dfd': True, 'm': 5},
         date='24012024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")

    # Synthetic
    main(data_name='synthetic', 
         datasets_names=['long_target_without', 'long_target_with', 'wide_target', 'desc_target_perfect', 'desc_target_medium'], 
         #datasets_names=['desc_target_perfect'], 
         synthetic_params = {'N': [10000], 'T': [10], 'G': [3], 'noise': [0.1], 'SGTypes': ['E']},
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [20], 'model': ['zmean_high'],
                       'dbs': [False], 'wcs': [False], 'gamma': [None], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]},           
         extra_info = {'target_column_names': ['Target','IDCode','TimeInd'], 'sample': None, 'run_beam_search': True, 'make_dfd': False, 'm': 5},
         date='25012024', 
         data_from="./data_input/",
         output_to="./output/")    

    # Synthetic
    main(data_name='synthetic', 
         #datasets_names=['long_target_without', 'long_target_with', 'wide_target', 'desc_target_perfect', 'desc_target_medium'], 
         datasets_names=['long_target_without'], 
         synthetic_params = {'N': [10000], 'T': [10], 'G': [3], 'noise': [0.1], 'SGTypes': ['E']},
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [20], 'model': ['zmean_high'],
                       'dbs': [False], 'wcs': [False], 'gamma': [None], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]},           
         extra_info = {'target_column_names': ['Target','IDCode','TimeInd'], 'sample': None, 'run_beam_search': True, 'make_dfd': True, 'm': 20},
         date='26012024', 
         data_from="./data_input/",
         output_to="./output/")

    # Synthetic
    main(data_name='synthetic', 
         #datasets_names=['long_adapt_without', 'long_adapt_with', 'wide_adapt', 'desc_adapt_perfect', 'desc_adapt_medium'], 
    '''
    # FUNA
    main(data_name='FUNA', 
         #datasets_names=['desc_adapt','desc','long_adapt','long','wide_adapt','wide','wide_10','wide_50','wide_90'],
         datasets_names=['desc_adapt', 'long_adapt','wide_adapt'],
         #datasets_names=['desc_target'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [5], 'd': [1], 'q': [5], 'model': ['subrange_fit', 'zsubrange', 'zmean_high'],
                       'dbs': [True], 'wcs': [True], 'gamma': [0.9], 'dp': [True], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'run_beam_search': True, 'make_dfd': False, 'm': 5},
         date='26012024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")

    