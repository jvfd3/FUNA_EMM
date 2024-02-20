import numpy as np
import pandas as pd

def remove_redundant_descriptions(descs=None, sel_params=None, stop_number_dbs=None):

    all_descs = descs.copy()

    if sel_params['d_i'] > 1:

        varphi_range = check_range(all_descs=all_descs, sel_params=sel_params)

        # even if the length of descs is small, we still want to remove redundant descriptions
        if len(all_descs) > stop_number_dbs:
            stop_at = stop_number_dbs
        else: 
            stop_at = len(all_descs)

        i = 1
        candidates = [all_descs[0]]
        n_redun_descs = 0
        while i < stop_at:
            #print(i)
            new_desc = all_descs[i]
            #print('new_desc', new_desc['description'])
            for old_desc in candidates:

                #if new_desc['qualities']['varphi'] == old_desc['qualities']['varphi']:
                are_equal = compare_two_varphi(varphi1=new_desc['qualities']['varphi'], varphi2=old_desc['qualities']['varphi'], varphi_range=varphi_range)
                if are_equal:

                    remove = compare_two_descs(old_desc=old_desc['description'], new_desc=new_desc['description'])
                    if remove == 'old_desc':
                        candidates.remove(eval(remove))
                        n_redun_descs += 1
                    elif remove == 'new_desc':
                        n_redun_descs += 1
                        break # return to while loop, break the for loop
                
                else:
                    remove = None
            
            if not remove == 'new_desc':                    
                candidates.append(new_desc)
            i += 1

    else:

        n_redun_descs = None
        candidates = all_descs[0:stop_number_dbs]

    return candidates, n_redun_descs

def check_range(all_descs=None, sel_params=None):

    # for now, very conservative, we take 0.05 from the maximum varphi that exists
    # it is just meant to correct for rounding error or scaling problems
    all_varphis = [desc['qualities']['varphi'] for desc in all_descs]
    max_varphi = np.max(all_varphis)
    varphi_range = sel_params['alpha'] * max_varphi

    return varphi_range

def compare_two_varphi(varphi1=None, varphi2=None, varphi_range=None):

    are_equal = False
    dif = np.abs(varphi1 - varphi2)
    if dif < varphi_range:
        are_equal = True

    return are_equal

def compare_two_descs(old_desc=None, new_desc=None):

    length_dif = len(new_desc) - len(old_desc)

    remove = None
    if np.abs(length_dif) > 1:
        remove = None

    # new_desc is smaller than old_desc
    # check if all items exist in old_desc
    # if so, the new_desc is a general description of old_desc
    elif length_dif == -1:
        items_exist_in_old_desc = [item in list(old_desc.items()) for item in list(new_desc.items())]
        #print('items_exist_in_old_desc', items_exist_in_old_desc)
        if np.all(items_exist_in_old_desc):
            remove = 'old_desc'

    # old_desc is smaller than new_desc
    # same procedure
    elif length_dif == 1:
        items_exist_in_new_desc = [item in list(new_desc.items()) for item in list(old_desc.items())]
        #print('items_exist_in_new_desc', items_exist_in_new_desc)
        if np.all(items_exist_in_new_desc):
            remove = 'new_desc'

    # check difference
    # if two or more keys are different, both can be kept
    # if two or more literals are different, both can be kept
    # otherwise, take the more general description
    elif length_dif == 0:
        same_keys = [key not in list(old_desc.keys()) for key in list(new_desc.keys())]
        #print('same_keys', same_keys)
        if np.sum(same_keys) < 2:
            same_descs = [item not in list(old_desc.items()) for item in list(new_desc.items())]
            #print('same_descs', same_descs)
            if np.sum(same_descs) == 1:
                # we know the difference is in the key difference, we remove the latest one
                remove = 'new_desc'
            elif np.sum(same_descs) == 0:
                # remove the more general description
                # bit complex to write, for convenience we remove the latest one
                remove = 'new_desc'
            else: 
                remove = None

    else:
        print('some mistake, new subgroup is larger than old subgroup')
        remove = None

    #print('remove', remove)

    return remove