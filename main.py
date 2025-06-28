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
    excel_file_name, sheet_names = ssr.create_empty_output_file(
        output_to_path=output_to_path)

    if synthetic_params is None:
        an.analysis(data_name=data_name, data_from=data_from, datasets_names=datasets_names, sim_params=sim_params,
                    extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    elif synthetic_params is not None:
        an.synthetic_analysis(datasets_names=datasets_names, synthetic_params=synthetic_params, data_from=data_from, sim_params=sim_params,
                              extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    ssr.final_update_result(
        excel_file_name=excel_file_name, sheet_names=sheet_names)


if __name__ == '__main__':
    '''   
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3, 5], 'q': [10], 'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1, 0.5, 0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': True, 
                       'run_beam_search': True, 'make_dfd': False, 'm': None}, 
         date='03032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''
    '''
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3, 5], 'q': [10], 'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb', 'subrange_fit'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1, 0.5, 0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': False, 
                       'run_beam_search': True, 'make_dfd': True, 'm': 50}, 
         date='05032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")

    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [20], 'model': ['subrange_ssrb'],  
                       'dbs': [False], 'wcs': [True], 'gamma': [0.5], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': False, 'sample_prop': None, 
                       'case_based_target': False, 'run_redun_metrics': False,
                       'run_beam_search': True, 'make_dfd': False, 'm': None}, 
         date='06032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''
    '''
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [5], 'q': [10], 'model': ['subrange_bic'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.5,0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': True, 
                       'run_beam_search': True, 'make_dfd': True, 'm': 2, 'startorder': 0, 'maxorder': 3}, 
         date='07032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    
    # do ssr again, with 1/ef instead of ef
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3, 5], 'q': [10], 'model': ['subrange_ssr'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1,0.5,0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': True, 
                       'run_beam_search': True, 'make_dfd': True, 'm': 50}, 
         date='08032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''
    main(data_name='Curran', 
        datasets_names=['desc'],
        synthetic_params = None,
        sim_params = {'b': [4], 'w': [20], 'd': [3, 5], 'q': [10], 'model': ['reg_ssr', 'reg_ssrb', 'reg_bic'],
                    'dbs': [False], 'alpha': [0.05], 'wcs': [True], 'gamma': [0.1,0.5,0.9], 'dp': [False], 'md': ['without'],
                    'min_size': [0.05]}, 
        extra_info = {'target_column_names': ['read','id','occasion','kidagetv'], 'sample': None, 
                    'prefclass': None, 'case_based_target': False, 'run_redun_metrics': True,
                    'run_beam_search': True, 'make_dfd': True, 'm': 2, 'startorder': 0, 'maxorder': 3}, 
        date='10032024', 
        data_from="/home/alexis/ufmg/2025-1/aprendizado-descritivo/seminarios/artigo6/FUNA_EMM/data_input/",
        output_to="./output/")

    '''
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [20], 'model': ['subrange_bic'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.5], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': False, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': False, 
                       'run_beam_search': True, 'make_dfd': False, 'm': 2, 'startorder': 0, 'maxorder': 3}, 
         date='10032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''
    '''
    main(data_name='Curran', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3, 5], 'q': [10], 'model': ['reg_ssr', 'reg_ssrb', 'reg_bic'],
                       'dbs': [False], 'alpha': [0.05], 'wcs': [True], 'gamma': [0.1,0.5,0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['read','id','occasion','kidagetv'], 'sample': None, 
                       'prefclass': None, 'case_based_target': False, 'run_redun_metrics': False,
                       'run_beam_search': True, 'make_dfd': True, 'm': 50, 'startorder': 0, 'maxorder': 3}, 
         date='11032024', 
         data_from="C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/FUNA_EMM/data_input/",
         output_to="./output/")
    '''
    '''
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3,5], 'q': [10], 'model': ['subrange_bic'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1,0.5,0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': False, 
                       'run_beam_search': True, 'make_dfd': True, 'm': 50, 'startorder': 0, 'maxorder': 3}, 
         date='11032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''
