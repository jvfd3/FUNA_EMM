import numpy as np
import pandas as pd

def select_using_weighted_coverage(candidates=None, general_params=None, stop_number_wcs=None, wcs_gamma=None):

    # if the number of candidates is smaller than the desired number, we can just select all candidates
    if len(candidates) > stop_number_wcs:

        allIDs = general_params['IDs']
        temp_allIDs = pd.DataFrame({'IDs': allIDs, 'count': np.zeros(len(allIDs))})

        selidxIDs = candidates[0]['adds']['idxIDs']['idx_id']
        sel = [candidates[0]]
        left_over_candidates = candidates.copy()
        left_over_candidates.remove(left_over_candidates[0])

        i = 1
    
        while i < stop_number_wcs:
       
            # update weight of cases coverd by already selected descriptions
            temp_allIDs.loc[temp_allIDs['IDs'].isin(selidxIDs),'count'] += 1
            candidates_with_updated_qms = []

            for candidate in left_over_candidates:
                
                # select rows in current candidate and calculate weight for candidate
                selidxIDs = candidate['adds']['idxIDs']['idx_id']
                all_weights = np.power(wcs_gamma, temp_allIDs.loc[temp_allIDs['IDs'].isin(selidxIDs),'count'].values)
                weight = np.sum(all_weights) / len(selidxIDs)

                # calculate new quality value with weight for subgroup
                candidate['qualities']['temp_varphi'] = candidate['qualities']['varphi'] * weight
                candidates_with_updated_qms.append(candidate)

            candidates_sorted = sorted(candidates_with_updated_qms, key = lambda i: i['qualities']['temp_varphi'], reverse=True)
            
            # select first candidate and update other lists
            selidxIDs = candidates_sorted[0]['adds']['idxIDs']['idx_id']
            sel.append(candidates_sorted[0])
            left_over_candidates.remove(candidates_sorted[0])

            i += 1

    else:

        sel = candidates

    return sel