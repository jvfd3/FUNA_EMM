import numpy as np
import pandas as pd

import constraints.desc_based_selection as dbs
import constraints.cover_based_selection as cbs

def prepare_beam_and_candidate_result_set(candidate_result_set=None, cq_satisfied=None, sel_params=None, general_params=None):
    
    candidate_queue = []
    n_redun_descs = None

    if len(cq_satisfied) > 0:

        cq_sorted = sort_list_on_quality(list_unsorted=cq_satisfied)
        #print(cq_sorted[0]['description'])
        #print(cq_sorted[0]['qualities']['varphi'])
        #print(len(cq_sorted[0]['adds']['idxIDs']['idx_id']))
    
        candidate_queue, n_redun_descs = apply_dbs_wcs(cq_sorted=cq_sorted, sel_params=sel_params, general_params=general_params, stop_number_dbs = 4*sel_params['w'], stop_number_wcs=sel_params['w'], wcs_gamma=sel_params['gamma'])

        # we have the same procedure for the result set, but we do that all the way at the end, because of possibly applying dominance pruning
        # for now, we therefore just prepare a list of possible results
        selected_for_result_list = candidate_queue[0:sel_params['q']]
        candidate_result_set.append(selected_for_result_list) # creates a nested list
        rs_candidates = [item for sublist in candidate_result_set for item in sublist] # unlist alle elements
        candidate_result_set = [rs_candidates]

        #print(candidate_queue[0]['description'])
        #print(candidate_queue[0]['qualities']['varphi'])
        #print(len(candidate_queue[0]['adds']['idxIDs']['idx_id']))

    return candidate_result_set, candidate_queue, n_redun_descs

def prepare_result_set(candidate_result_set=None, general_params=None, sel_params=None):

    result_set_ordered = sort_list_on_quality(list_unsorted=candidate_result_set)

    # here 'w' is replaced with 'q'
    result_set, rs_n_redun_descs = apply_dbs_wcs(cq_sorted=result_set_ordered, sel_params=sel_params, general_params=general_params, stop_number_dbs = 4*sel_params['q'], stop_number_wcs=sel_params['q'], wcs_gamma=sel_params['gamma'])

    return result_set, rs_n_redun_descs

def sort_list_on_quality(list_unsorted=None):

    # sort cq_satisfied on quality value
    list_sorted = sorted(list_unsorted, key=lambda i: i['qualities']['varphi'], reverse=True) 

    return list_sorted

def apply_dbs_wcs(cq_sorted=None, sel_params=None, general_params=None, stop_number_dbs=None, stop_number_wcs=None, wcs_gamma=None):

    # apply description-based selection
    if sel_params['dbs']:
        # difficult to know when to stop
        # only from 2nd level and onwards
        candidates, n_redun_descs = dbs.remove_redundant_descriptions(descs=cq_sorted, sel_params=sel_params, stop_number_dbs=stop_number_dbs)
    else: 
        candidates = cq_sorted[0:stop_number_dbs]
        n_redun_descs = None

    # apply cover-based selection
    if sel_params['wcs']:         
        # len(candidates) should always be larger than 0, at least 1 description will be maintained
        candidate_queue = cbs.select_using_weighted_coverage(candidates=candidates, sel_params=sel_params, general_params=general_params, stop_number_wcs=stop_number_wcs,  wcs_gamma=wcs_gamma)
    else: 
        candidate_queue = candidates[0:stop_number_wcs]

    return candidate_queue, n_redun_descs
    