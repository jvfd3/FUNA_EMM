import numpy as np
import pandas as pd

from joblib import Parallel, delayed

import beam_search.qualities as qu
import beam_search.refinements as rf
import beam_search.select_subgroup as ss
import beam_search.prepare_beam as pb
import beam_search.summarize as sm
import constraints.dominance_pruning as dp
import constraints.constraints as cs

def beam_search(target=None, attributes=None, descriptive=None, sel_params=None, extra_info=None):

    #print(target.shape) # target space pd dataframe
    #print(attributes) # dict with lists of attributes
    #print(descriptive.shape) # descriptive space pd dataframe

    target.reset_index(inplace=True,drop=True)
    descriptive.reset_index(inplace=True,drop=True)

    general_params = qu.calculate_general_params(target=target, sel_params=sel_params, extra_info=extra_info)
    #print(general_params['estimates']) # dictionary

    # check if md == 'knn':
    if sel_params['md'] == 'knn':
        descriptive = descriptive.copy() # perform knn
    
    candidate_queue = rf.create_starting_descriptions(descriptive=descriptive, attributes=attributes, b=sel_params['b'], md=sel_params['md'])
    #print(candidate_queue)

    candidate_result_set = []
    considered_subgroups = {}    

    for d_i in range(1, sel_params['d']+1):
        
        #print('d_i', d_i)
        n_consd = 0
        n_sim_descs = 0
        n_small_groups = 0

        cq_satisfied = []
        for seed in candidate_queue:
            
            if d_i == 1:
                seed_set = []
                seed_set.append(seed)
            else:                
                subgroup, idxIDs, subgroup_compl, idx_compl = ss.select_subgroup(description=seed['description'], df=descriptive, attributes=attributes)
                seed_set = rf.refine_seed(seed=seed, subgroup=subgroup, attributes=attributes, b=sel_params['b'], md=sel_params['md'])

            for desc in seed_set:

                #print(desc)

                n_consd += 1

                # check for similar description
                constraint_similar_description = cs.check_similar_description(desc=desc, cq_satisfied=cq_satisfied, d_i=d_i, current_beam=candidate_queue)
                if constraint_similar_description:
                    n_sim_descs += 1
                else: 
                    desc_qm, constraint_subgroup_size, n_small_groups = qu.evaluate_desc(desc=desc, descriptive=descriptive, attributes=attributes, target=target, 
                                                                                         sel_params=sel_params, general_params=general_params, 
                                                                                         extra_info=extra_info, n_small_groups=n_small_groups)
                    if not constraint_subgroup_size:
                        cq_satisfied.append(desc_qm)
                        #print(desc_qm['qualities'])

        sel_params.update({'d_i': d_i})
                                                     
        #print('start preparing beam')
        candidate_result_set, candidate_queue, n_redun_descs = pb.prepare_beam_and_candidate_result_set(candidate_result_set= candidate_result_set, 
                                                                                                        cq_satisfied=cq_satisfied, sel_params=sel_params, 
                                                                                                        general_params=general_params)

        considered_subgroups['level_' + str(d_i)] = {'n_consd': n_consd, 'n_sim_descs': n_sim_descs, 'n_small_groups': n_small_groups, 'n_redun_decs': n_redun_descs}                            
    
    #print('prepare result set')
    result_set, n_redun_descs = pb.prepare_result_set(candidate_result_set=candidate_result_set[0], sel_params=sel_params, general_params=general_params)
    considered_subgroups['level_' + str(d_i)].update({'n_redun_descs': n_redun_descs})
   
    # apply dominance pruning
    if sel_params['dp']:    
        result_set, considered_subgroups = dp.apply_dominance_pruning(result_set=result_set, considered_subgroups=considered_subgroups, sel_params=sel_params, extra_info=extra_info, 
                                                                      descriptive=descriptive, target=target, attributes=attributes, general_params=general_params)  
        
    # result_set is a dictionary
    # result_emm is a dataframe 
    result_emm = sm.result_set_to_df(result_set=result_set)

    return result_emm, general_params, considered_subgroups





    