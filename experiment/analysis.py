import numpy as np
import pandas as pd
import itertools as it
import time

import experiment.retrieve_rw_data as rd
import experiment.retrieve_synthetic_data as sd
import beam_search.beam_search as bs
import experiment.distribution_false_discoveries as dfd

def synthetic_analysis(datasets_names=None, synthetic_params=None, data_from=None, simulation_params=None, beam_search_params=None, model_params=None, alg_constraints=None, dfd_params=None, wcs_params=None):

    syn_simulation_result = []
    synparamset = list(it.product(synthetic_params['N'], synthetic_params['T'], synthetic_params['G'], synthetic_params['minsize'], synthetic_params['noise']))
    desc_keys = datasets_names
        
    h = 1
    for synparams in synparamset:

        print('Data created for', h, 'out of', len(synparamset), ' combinations:', synparams)      

        if synparams[3] == 'default': 
            alg_constraints['min_size'] = 0.05
        elif synparams[3] == 'adapted': 
            # adapt min_size to G^T
            alg_constraints['min_size'] = 1/((synparams[2]**synparams[1])+1)

        # create or extract data
        # this dataset contains synthetic_params['SGTypes'] number of subgroup types
        descriptive_datasets, attribute_sets, target, syn_data_at_path = sd.retrieve_synthetic_data(data_from=data_from, synparams=synparams, datasets_names=datasets_names)

        all_types = synthetic_params['SGTypes'].copy()
        
        j = 1
        for subgroup_type in synthetic_params['SGTypes']:
            synparamstype = synparams + tuple(subgroup_type)
            print('Simulation for ', j, 'out of', len(synthetic_params['SGTypes']), ' subgroup types:', subgroup_type)  

            all_types.remove(subgroup_type)
            selcolumns = ['Target'+sg for sg in all_types]

            targettype = target.copy()
            targettype.drop(columns=selcolumns,axis=1, inplace=True)
            targettype.rename({'Target'+subgroup_type:'Target'},axis=1,inplace=True)

            # start analysis
            single_simulation_result = analysis_per_dataset(descriptive_datasets=descriptive_datasets, attribute_sets=attribute_sets, target=targettype, simulation_params=simulation_params, 
                                                            beam_search_params=beam_search_params, model_params=model_params, wcs_params=wcs_params, dfd_params=dfd_params, alg_constraints=alg_constraints)
            syn_simulation_result.append({'synparams': synparamstype, 'single_simulation_result': single_simulation_result, 'syn_data_at_path': syn_data_at_path})

            j += 1

        h += 1

    return syn_simulation_result

def analysis(data_name=None, data_from=None, datasets_names=None, simulation_params=None, beam_search_params=None, model_params=None, alg_constraints=None, dfd_params=None, wcs_params=None):

    descriptive_datasets, attribute_sets, target = rd.retrieve_rw_data(data_name=data_name, data_from=data_from, datasets_names=datasets_names, sample=simulation_params['sample'])
    simulation_result = analysis_per_dataset(descriptive_datasets=descriptive_datasets, attribute_sets=attribute_sets, target=target, simulation_params=simulation_params, 
                                             beam_search_params=beam_search_params, model_params=model_params, wcs_params=wcs_params, dfd_params=dfd_params, alg_constraints=alg_constraints)

    return simulation_result

def analysis_per_dataset(descriptive_datasets=None, attribute_sets=None, target=None, simulation_params=None, beam_search_params=None, model_params=None, wcs_params=None, dfd_params=None, alg_constraints=None):

    desc_keys = descriptive_datasets.keys()
    # order is important! 
    paramset = list(it.product(list(desc_keys), simulation_params['dbs'], simulation_params['wcs'], simulation_params['dp'], simulation_params['md'], simulation_params['target_model'])) 

    i = 1
    simulation_result = []
    for params in paramset:
        
        params = list(params)
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

        simulation_result.append({'params': params, 'result_emm': result_emm, 'general_params': general_params, 'considered_subgroups': considered_subgroups, 'time': elapsed_time, 'distribution': distribution, 'attributes': attribute_sets[params[0]]})

        i += 1

    return simulation_result