import numpy as np
import pandas as pd


def select_using_weighted_coverage(candidates=None, sel_params=None, general_params=None, stop_number_wcs=None, wcs_gamma=None):

    if 'long' in sel_params['data_key']:
        data_idx_col = 'idx'
        sg_idx_col = 'idx_sg'
        allIDs = np.arange(0, general_params['nrrows'])
    else:
        data_idx_col = 'IDs'
        sg_idx_col = 'idx_id'
        allIDs = general_params[data_idx_col]

    # if the number of candidates is smaller than the desired number, we can just select all candidates
    if len(candidates) > stop_number_wcs:

        temp_allIDs = pd.DataFrame(
            {data_idx_col: allIDs, 'count': np.zeros(len(allIDs))})

        selidxIDs = candidates[0]['adds']['idxIDs'][sg_idx_col]
        sel = [candidates[0]]
        # print(sel[0]['description'])
        left_over_candidates = candidates.copy()
        left_over_candidates.remove(left_over_candidates[0])

        i = 1

        while i < stop_number_wcs:

            # print('i:', i)

            # update weight of cases coverd by already selected descriptions
            temp_allIDs.loc[temp_allIDs[data_idx_col].isin(
                selidxIDs), 'count'] += 1
            candidates_with_updated_qms = []

            j = 0
            for candidate in left_over_candidates:
                # print('j:', j)
                # select rows in current candidate and calculate weight for candidate
                selidxIDs = candidate['adds']['idxIDs'][sg_idx_col]
                # print(candidate['description'])
                # print(temp_allIDs.loc[temp_allIDs[data_idx_col].isin(selidxIDs),'count'].values)
                all_weights = np.power(
                    wcs_gamma, temp_allIDs.loc[temp_allIDs[data_idx_col].isin(selidxIDs), 'count'].values)
                weight = np.sum(all_weights) / len(selidxIDs)
                # print(weight)

                # calculate new quality value with weight for subgroup
                candidate['qualities']['temp_varphi'] = candidate['qualities']['varphi'] * weight
                candidates_with_updated_qms.append(candidate)
                j += 1

            candidates_sorted = sorted(
                candidates_with_updated_qms, key=lambda i: i['qualities']['temp_varphi'], reverse=True)

            # select first candidate and update other lists
            selidxIDs = candidates_sorted[0]['adds']['idxIDs'][sg_idx_col]
            sel.append(candidates_sorted[0])
            # print(candidates_sorted[0]['description'])
            left_over_candidates.remove(candidates_sorted[0])

            i += 1

    else:

        sel = candidates

    return sel
