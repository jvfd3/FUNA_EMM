import numpy as np
import pandas as pd

import beam_search.qualities as qu
import beam_search.refinements as rf
import beam_search.select_subgroup as ss
import beam_search.prepare_beam as pb
import beam_search.summarize as sm
import constraints.dominance_pruning as dp
import constraints.constraints as cs

def beam_search(target=None, attributes=None, descriptive=None, sim_params=None, beam_search_params=None, model_params=None, wcs_params=None, alg_constraints=None):

    #print(target.shape) # target space pd dataframe
    #print(attributes) # dict with lists of attributes
    #print(descriptive.shape) # descriptive space pd dataframe

    target.reset_index(inplace=True,drop=True)
    descriptive.reset_index(inplace=True,drop=True)

    general_params = qu.calculate_general_params(target=target, model_params=model_params)
    #print(general_params['estimates']) # dictionary

    # check if md == 'knn':
    if sim_params[4] == 'knn':
        descriptive = descriptive.copy() # perform knn
    
    candidate_queue = rf.create_starting_descriptions(descriptive=descriptive, attributes=attributes, b=beam_search_params['b'], md=sim_params[4])
    #print(candidate_queue)

    candidate_result_set = []
    considered_subgroups = {}    

    for d_i in range(1, beam_search_params['d']+1):
        
        #print('d_i', d_i)
        n_consd = 0
        n_sim_descs = 0
        n_small_groups = 0
        
        cq_satisfied = []
        for seed in candidate_queue:

            #print('seed', seed['description'])

            if d_i == 1:
                seed_set = []
                seed_set.append(seed)
            else:                
                subgroup, idxIDs, subgroup_compl, idx_compl = ss.select_subgroup(description=seed['description'], df=descriptive, attributes=attributes)
                seed_set = rf.refine_seed(seed=seed, subgroup=subgroup, attributes=attributes, b=beam_search_params['b'], md=sim_params[4])

            for desc in seed_set:

                n_consd += 1

                # check for similar description
                constraint_similar_description = cs.check_similar_description(desc=desc, cq_satisfied=cq_satisfied)
                if constraint_similar_description:
                    n_sim_descs += 1
                else: 
                    desc_qm, constraint_subgroup_size, n_small_groups = qu.evaluate_desc(desc=desc, descriptive=descriptive, attributes=attributes, target=target, model_params=model_params, general_params=general_params, alg_constraints=alg_constraints, n_small_groups=n_small_groups)
                    if not constraint_subgroup_size:
                        cq_satisfied.append(desc_qm)

        beam_search_params.update({'d_i': d_i})
                                                     
        #print('start preparing beam')
        candidate_result_set, candidate_queue, n_redun_descs = pb.prepare_beam_and_candidate_result_set(candidate_result_set= candidate_result_set, cq_satisfied=cq_satisfied, sim_params=sim_params, beam_search_params=beam_search_params, general_params=general_params, wcs_params=wcs_params)

        considered_subgroups['level_' + str(d_i)] = {'n_consd': n_consd, 'n_sim_descs': n_sim_descs, 'n_small_groups': n_small_groups, 'n_redun_decs': n_redun_descs}                            
    
    #print('prepare result set')
    result_set, n_redun_descs = pb.prepare_result_set(candidate_result_set=candidate_result_set[0], beam_search_params=beam_search_params, sim_params=sim_params, wcs_params=wcs_params, general_params=general_params)
    considered_subgroups['level_' + str(d_i)].update({'n_redun_descs': n_redun_descs})
   
    # apply dominance pruning
    if sim_params[3]:    
        result_set, considered_subgroups = dp.apply_dominance_pruning(result_set=result_set, considered_subgroups=considered_subgroups, beam_search_params=beam_search_params, sim_params=sim_params, wcs_params=wcs_params, descriptive=descriptive, target=target, attributes=attributes, model_params=model_params, general_params=general_params, alg_constraints=alg_constraints)  
        
    # result_set is a dictionary
    # result_emm is a dataframe 
    result_emm = sm.result_set_to_df(result_set=result_set)

    return result_emm, general_params, considered_subgroups





    