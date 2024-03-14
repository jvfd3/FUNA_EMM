import numpy as np
import pandas as pd
import itertools as it
import time
import os

import experiment.retrieve_rw_data as rd
import beam_search.beam_search as bs
import experiment.distribution_false_discoveries as dfd
import experiment.save_and_store_result as ssr

def analysis(data_name=None, data_from=None, datasets_names=None, sim_params=None, extra_info=None, output_to_path=None, excel_file_name=None, sheet_names=None):

    descriptive_datasets, attribute_sets, target = rd.retrieve_rw_data(data_name=data_name, data_from=data_from, datasets_names=datasets_names, extra_info=extra_info)
    simulation_result = analysis_per_dataset(descriptive_datasets=descriptive_datasets, attribute_sets=attribute_sets, target=target, 
                                             sim_params=sim_params, extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    return simulation_result

def analysis_per_dataset(descriptive_datasets=None, attribute_sets=None, target=None, sim_params=None,
                         extra_info=None, output_to_path=None, excel_file_name=None, sheet_names=None):

    desc_keys = descriptive_datasets.keys()
    #print(attribute_sets)
    #print(descriptive_datasets)
    
    k = 1
    for desc_key in desc_keys:

        print('Data format', k, 'out of', len(desc_keys), ':', desc_key)  

        # results are stored after every type of data format
        output_to_desc_key_path = output_to_path + desc_key + '/'
        if not os.path.exists(output_to_desc_key_path):
            os.makedirs(output_to_desc_key_path) 
    
        sim_values = list(sim_params.values())
        paramset = list(it.product(*sim_values))

        i = 1
        #simulation_result = []
        for params in paramset:
        
            #params = [desc_key] + list(params)
            print('Simulation', i, 'out of', len(paramset), ':', params)     

            sel_params = prepare_sel_params(desc_key=desc_key, params=params, keys=list(sim_params.keys()))

            distribution=None  
            result_emm=None
            elapsed_time=0

            #print(attribute_sets[sel_params['data_key']])
            #print(descriptive_datasets[sel_params['data_key']])

            # a single run
            if extra_info['run_beam_search']:
                #print('start beam search')
                st = time.time()
                result_emm, general_params, considered_subgroups = bs.beam_search(target=target, attributes=attribute_sets[sel_params['data_key']], 
                                                                                  descriptive=descriptive_datasets[sel_params['data_key']], sel_params=sel_params, 
                                                                                  extra_info=extra_info) 
                                                                                  #beam_search_params=sel_beam_search_params, model_params=sel_model_params, 
                                                                                  #wcs_params=sel_wcs_params, alg_constraints=sel_alg_constraints)
                et = time.time()
                elapsed_time = et - st
                print('Execution time:', elapsed_time, 'seconds')
                #print(result_emm['varphi'])

            # check if distribution has to be made
            if extra_info['make_dfd']:
                # build dfd, as a pd.DataFrame where the quality values are a list, and other values are distribution params
                '''
                distribution = dfd.distribution_false_discoveries_params(m=extra_info['m'], target=target, attributes=attribute_sets[sel_params['data_key']], 
                                                                         descriptive=descriptive_datasets[sel_params['data_key']], sel_params=sel_params, 
                                                                         extra_info=extra_info) 
                '''
                distribution = dfd.distribution_false_discoveries_params_without(m=extra_info['m'], target=target, attributes=attribute_sets[sel_params['data_key']], 
                                                                         descriptive=descriptive_datasets[sel_params['data_key']], sel_params=sel_params, 
                                                                         extra_info=extra_info)

            simulation_result = {'params': sel_params, 'result_emm': result_emm, 'general_params': general_params, 'considered_subgroups': considered_subgroups, 
                                 'time': elapsed_time, 'distribution': distribution, 'attributes': attribute_sets[sel_params['data_key']]}
            ssr.save_and_store_result(simulation_result=simulation_result, extra_info=extra_info,
                                      output_to_path=output_to_desc_key_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

            i += 1

        k += 1

        #simulation_summary, distribution_summary, info_summary = ssr.save_and_store_result(simulation_result=simulation_result, output_to_path=output_to_desc_key_path)        

    return True

def prepare_sel_params(desc_key=None, params=None, keys=None):

    sel_params = {'data_key': desc_key}
    sel_params.update({key:value for key,value in zip(keys,params)})
    
    return sel_params
