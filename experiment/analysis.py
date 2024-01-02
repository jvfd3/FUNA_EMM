import numpy as np
import pandas as pd
import itertools as it
import time
import os

import experiment.retrieve_rw_data as rd
import experiment.retrieve_synthetic_data as sd
import beam_search.beam_search as bs
import experiment.distribution_false_discoveries as dfd
import experiment.save_and_store_result as ssr

def synthetic_analysis(datasets_names=None, synthetic_params=None, data_from=None, simulation_params=None, beam_search_params=None, model_params=None, alg_constraints=None, 
                       dfd_params=None, wcs_params=None, output_to_path=None, excel_file_name=None, sheet_names=None):

    syn_simulation_result = []
    synparamset = list(it.product(synthetic_params['N'], synthetic_params['T'], synthetic_params['G'], synthetic_params['minsize'], synthetic_params['noise']))
    desc_keys = datasets_names
        
    h = 1
    for synparams in synparamset: 

        if synparams[3] == 'default': 
            alg_constraints['min_size'] = 0.05
        elif synparams[3] == 'adapted': 
            # adapt min_size to G^T
            alg_constraints['min_size'] = 1/((synparams[2]**synparams[1])+1)

        # create or extract data
        # this dataset contains synthetic_params['SGTypes'] number of subgroup types
        print('Data is generated for', h, 'out of', len(synparamset), 'combinations:', synparams)      
        descriptive_datasets, attribute_sets, target, syn_data_at_path = sd.retrieve_synthetic_data(data_from=data_from, synparams=synparams, datasets_names=datasets_names)
       
        j = 1
        SGTypes = synthetic_params['SGTypes'].copy()
        for subgroup_type in synthetic_params['SGTypes']:
            synparamstype = synparams + tuple(subgroup_type)
            print('Simulation for ', j, 'out of', len(SGTypes), 'subgroup types:', subgroup_type) 

            output_to_syn_path = output_to_path + str(list(synparamstype)) + '/'
            if not os.path.exists(output_to_syn_path):
                os.makedirs(output_to_syn_path)  

            SGTypes.remove(subgroup_type)
            selcolumns = ['Target'+sg for sg in SGTypes]

            targettype = target.copy()
            targettype.drop(columns=selcolumns,axis=1, inplace=True)
            targettype.rename({'Target'+subgroup_type:'Target'},axis=1,inplace=True)

            # start analysis
            analysis_per_dataset(descriptive_datasets=descriptive_datasets, attribute_sets=attribute_sets, target=targettype, simulation_params=simulation_params, 
                                 beam_search_params=beam_search_params, model_params=model_params, wcs_params=wcs_params, 
                                 dfd_params=dfd_params, alg_constraints=alg_constraints, output_to_path=output_to_syn_path, excel_file_name=excel_file_name, sheet_names=sheet_names)
            
            j += 1    

        h += 1
    
    # add columns with synthetic params to output
    ssr.update_info_about_synthetic_result(synparamset=synparamset, SGTypes=synthetic_params['SGTypes'], excel_file_name=excel_file_name, sheet_names=sheet_names)

    return True

def analysis(data_name=None, data_from=None, datasets_names=None, simulation_params=None, beam_search_params=None, model_params=None, alg_constraints=None, 
             dfd_params=None, wcs_params=None, output_to_path=None, excel_file_name=None, sheet_names=None):

    descriptive_datasets, attribute_sets, target = rd.retrieve_rw_data(data_name=data_name, data_from=data_from, datasets_names=datasets_names, sample=simulation_params['sample'])
    simulation_result = analysis_per_dataset(descriptive_datasets=descriptive_datasets, attribute_sets=attribute_sets, target=target, simulation_params=simulation_params, 
                                             beam_search_params=beam_search_params, model_params=model_params, wcs_params=wcs_params, 
                                             dfd_params=dfd_params, alg_constraints=alg_constraints, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    return simulation_result

def analysis_per_dataset(descriptive_datasets=None, attribute_sets=None, target=None, simulation_params=None, beam_search_params=None, model_params=None, wcs_params=None, 
                         dfd_params=None, alg_constraints=None, output_to_path=None, excel_file_name=None, sheet_names=None):

    desc_keys = descriptive_datasets.keys()
    
    k = 1
    for desc_key in desc_keys:

        print('Data format', k, 'out of', len(desc_keys), ':', desc_key)  

        # results are stored after every type of data format
        output_to_desc_key_path = output_to_path + desc_key + '/'
        if not os.path.exists(output_to_desc_key_path):
            os.makedirs(output_to_desc_key_path) 
    
        #paramset = list(it.product(list(desc_keys), simulation_params['dbs'], simulation_params['wcs'], simulation_params['dp'], simulation_params['md'], simulation_params['target_model']))
        paramset = list(it.product(simulation_params['dbs'], simulation_params['wcs'], simulation_params['dp'], simulation_params['md'], simulation_params['target_model'])) 

        i = 1
        #simulation_result = []
        for params in paramset:
        
            params = [desc_key] + list(params)
            print('Simulation', i, 'out of', len(paramset), ':', params)     

            model_params['model'] = params[5]

            distribution=None  
            result_emm=None
            elapsed_time=0

            # a single run
            if dfd_params['make_normal']:
                #print('start beam search')
                st = time.time()
                result_emm, general_params, considered_subgroups = bs.beam_search(target=target, attributes=attribute_sets[params[0]], descriptive=descriptive_datasets[params[0]], sim_params=params, beam_search_params=beam_search_params, model_params=model_params, wcs_params=wcs_params, alg_constraints=alg_constraints)
                et = time.time()
                elapsed_time = et - st
                #print('Execution time:', elapsed_time, 'seconds')

            # check if distribution has to be made
            if dfd_params['make_dfd']:
                # build dfd, as a pd.DataFrame where the quality values are a list, and other values are distribution params
                distribution = dfd.distribution_false_discoveries_params(m=dfd_params['m'], target=target, attributes=attribute_sets[params[0]], descriptive=descriptive_datasets[params[0]], sim_params=params, beam_search_params=beam_search_params, model_params=model_params, wcs_params=wcs_params, alg_constraints=alg_constraints) 

            # simulation_result.append({'params': params, 'result_emm': result_emm, 'general_params': general_params, 'considered_subgroups': considered_subgroups, 'time': elapsed_time, 'distribution': distribution, 'attributes': attribute_sets[params[0]]})
            simulation_result = {'params': params, 'result_emm': result_emm, 'general_params': general_params, 'considered_subgroups': considered_subgroups, 'time': elapsed_time, 'distribution': distribution, 'attributes': attribute_sets[params[0]]}
            ssr.save_and_store_result(simulation_result=simulation_result, output_to_path=output_to_desc_key_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

            i += 1

        k += 1

        #simulation_summary, distribution_summary, info_summary = ssr.save_and_store_result(simulation_result=simulation_result, output_to_path=output_to_desc_key_path)        

    return True