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
    ''' 
    '''
    # FUNA
    # difference with before: wcs changed for long format, we set gamma = 0.5, we provide full_target possibility, adapt version is now linked per item-number
    main(data_name='FUNA',
         #datasets_names=['long_adapt_with','long_adapt_full_target_with','long_with','long_full_target_with', 
         #                'long_adapt_without','long_adapt_full_target_without','long_without','long_full_target_without',
         #                'desc_adapt','desc',
         #                'wide','wide_10','wide_50','wide_adapt','wide_90'],
         datasets_names=['long_adapt_with','long_adapt_full_target_with','long_with','long_full_target_with', 
                         'long_adapt_without','long_adapt_full_target_without','long_without','long_full_target_without',
                         'desc_adapt','desc',
                         'wide','wide_10','wide_50','wide_adapt','wide_90'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['zmean_high'],
                       'dbs': [True], 'wcs': [True], 'gamma': [0.5], 'dp': [True], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'run_beam_search': True, 'make_dfd': True, 'm': 20}, 
         date='30012024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    
    # This run is closer to what Pekka is searching for
    # we cannot include wide data, too many descriptors
    # we will not include long data, interpretation is not very meaningfull
    # we will not sample, hence, use 15485 cases and NC and arithmetic descriptors
    main(data_name='FUNA', 
         #datasets_names=['long_adapt_with','long_adapt_full_target_with','long_with','long_full_target_with', 
         #                'long_adapt_without','long_adapt_full_target_without','long_without','long_full_target_without',
         #                'desc_adapt','desc',
         #                'wide','wide_10','wide_50','wide_adapt','wide_90'],
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['subrange_fit'],
                       'dbs': [True], 'wcs': [True], 'gamma': [0.5], 'dp': [True], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': False, 'run_beam_search': True, 'make_dfd': True, 'm': 20}, 
         date='01022024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''
    '''
    # This is run but not yet evaluated; will probably not focus on dbs and wcs for this paper
    # Synthetic
    # the non-adapt versions do not exist for synthetic data
    main(data_name='synthetic', 
         datasets_names=['desc_adapt_perfect', 'desc_adapt_medium',
                         'long_adapt_full_target_without', 'long_adapt_full_target_with', 'long_adapt_without', 'long_adapt_with', 
                         'wide_adapt'], 
         synthetic_params = {'N': [10000], 'T': [10], 'G': [3], 'noise': [0.1], 'SGTypes': ['D']},
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['zslope_high'],
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1,0.5,0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]},           
         extra_info = {'target_column_names': ['Target','IDCode','TimeInd'], 'sample': None, 'run_beam_search': True, 'make_dfd': True, 'm': 10},
         date='02022024', 
         data_from="./data_input/",
         output_to="./output/")

    # This not yet evaluated in detail; wide and desc formats result in non-significant subgroups for low and high target models     
    main(data_name='FUNA', 
         #datasets_names=['long_adapt_with','long_adapt_full_target_with','long_with','long_full_target_with', 
         #                'long_adapt_without','long_adapt_full_target_without','long_without','long_full_target_without',
         #                'desc_adapt','desc',
         #                'wide','wide_10','wide_50','wide_adapt','wide_90'],
         datasets_names=['long_full_target_with', 'long_full_target_without', 'wide', 'desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['zsubrange_low', 'zsubrange_high', 'subrange_fit'],
                       'dbs': [True], 'wcs': [True], 'gamma': [0.5], 'dp': [True], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'run_beam_search': True, 'make_dfd': True, 'm': 20}, 
         date='03022024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''
    '''
    # changed dbs to have 4w instead of 2w
    # added 0.05 marge around dbs
    main(data_name='GPA/admitted', 
         datasets_names=['wide', 'desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [25], 'model': ['wra'],
                       'dbs': [True,False], 'alpha': [0.05], 'wcs': [True,False], 'gamma': [0.5], 'dp': [True,False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['admitted','student','semester'], 'sample': None, 'prefclass': 1.0, 'case_based_target': True,
                       'run_beam_search': True, 'make_dfd': True, 'm': 500}, 
         date='06022024', 
         data_from="C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/data_input/",
         output_to="./output/")
    '''
    '''
    main(data_name='GPA/gpa', 
         datasets_names=['wide', 'long_with', 'long_without', 'desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['zmean_high', 'zslope_high'],
                       'dbs': [False], 'alpha': [0.05], 'wcs': [False], 'gamma': [0.5], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['gpa','student','semester'], 'sample': None, 'prefclass': None, 'case_based_target': False,
                       'run_beam_search': True, 'make_dfd': True, 'm': 100}, 
         date='07022024', 
         data_from="C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/data_input/",
         output_to="./output/")
    
    main(data_name='Curran', 
         datasets_names=['wide', 'long_with', 'long_without', 'desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['zmean_high', 'zslope_high'],
                       'dbs': [False], 'alpha': [0.05], 'wcs': [False], 'gamma': [0.5], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['read','id','occasion'], 'sample': None, 'prefclass': None, 'case_based_target': False,
                       'run_beam_search': True, 'make_dfd': True, 'm': 100}, 
         date='08022024', 
         data_from="C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/DescriptionModels/data_input/",
         output_to="./output/")
    '''   
    '''
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [20], 'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb', 'subrange_fit'],  
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': False, 'sample_prop': None, 
                       'case_based_target': False, 'run_redun_metrics': False,
                       'run_beam_search': True, 'make_dfd': False, 'm': None}, 
         date='26022024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")

    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb', 'subrange_fit'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': False,
                       'run_beam_search': True, 'make_dfd': True, 'm': 20}, 
         date='27022024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3,5], 'q': [10], 'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb', 'subrange_fit'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1, 0.5, 0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': True, 
                       'run_beam_search': True, 'make_dfd': False, 'm': None}, 
         date='28022024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3,5], 'q': [10], 'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb', 'subrange_fit'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1,0.5,0.9], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.10, 
                       'case_based_target': False, 'run_redun_metrics': True, 
                       'run_beam_search': True, 'make_dfd': False, 'm': None}, 
         date='29022024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    '''
    '''
    # run with only 1 breakpoint in both subgroup and omega, we do not have to repeat for subrange_fit
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [5], 'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb'], 
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': True, 'sample_prop': 0.05, 
                       'case_based_target': False, 'run_redun_metrics': False,
                       'run_beam_search': True, 'make_dfd': True, 'm': 20}, 
         date='02032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
    
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
    
    main(data_name='FUNA', 
         datasets_names=['desc'],
         synthetic_params = None,
         sim_params = {'b': [4], 'w': [20], 'd': [3], 'q': [20], 'model': ['subrange_ll', 'subrange_ssr', 'subrange_ssrb'],  
                       'dbs': [False], 'wcs': [True], 'gamma': [0.1], 'dp': [False], 'md': ['without'],
                       'min_size': [0.05]}, 
         extra_info = {'target_column_names': ['DMTime','IDCode','PreOrd', 'DMStimL'], 'sample': False, 'sample_prop': None, 
                       'case_based_target': False, 'run_redun_metrics': False,
                       'run_beam_search': True, 'make_dfd': False, 'm': None}, 
         date='01032024', 
         data_from="C:/Users/20200059/Documents/Data/",
         output_to="./output/")
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
    
