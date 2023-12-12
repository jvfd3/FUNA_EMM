import numpy as np
import pandas as pd

def select_subgroup(description=None, df=None, attributes=None):

    pairs = list(description.items())

    num_atts = attributes['num_atts']
    bin_atts = attributes['bin_atts']
    nom_atts = attributes['nom_atts']
    ord_atts = attributes['ord_atts']

    if len(pairs) == 0:
        idx = []
    else: 
        # select all indices as a starting point
        idx = df.index.values

        for pair in pairs:

            att = pair[0]
            sel = pair[1]#[0] #sel[1][1] contains the order of the literal

            if att in bin_atts:
            
                idx = select_bin_att(idx=idx, att=att, sel=sel, df=df)
        
            elif att in num_atts:

                idx = select_num_att(idx=idx, att=att, sel=sel, df=df)

            elif att in nom_atts:

                idx = select_nom_att(idx=idx, att=att, sel=sel, df=df)

            elif att in ord_atts:

                idx = select_ord_att(idx=idx, att=att, sel=sel, df=df)
     
    all_idx = df.index.values
    idx_compl = np.setdiff1d(all_idx, idx)
    
    # this should be loc!!
    # make sure the dataset is sorted at the beginning of the algorithm
    subgroup = df.loc[idx]
    subgroup_compl = df.loc[idx_compl]

    idxIDs = transform_idx_to_IDs(subgroup=subgroup, id_atts=attributes['id_atts'], data_size_id=len(df[attributes['id_atts'][0]].unique()), data_size_rows=len(all_idx))

    return subgroup, idxIDs, subgroup_compl, list(idx_compl)

def transform_idx_to_IDs(subgroup=None, id_atts=None, data_size_id=None, data_size_rows=None):

    idxIDs = {'id_atts': id_atts,
              'idx_sg': list(subgroup.index.values),
              'idx_id': list(subgroup[id_atts[0]].unique())}
    idxIDs['size_sg'] = len(idxIDs['idx_id']) / data_size_id
    idxIDs['size_sg_rows'] = len(subgroup) / data_size_rows

    # in case of long descriptive data, time counter is an id attribute as well
    if len(id_atts) == 2:
        idxIDs['idx_combi'] = subgroup[id_atts].apply(tuple,axis=1)
    
    return idxIDs

def select_subgroup_part_of_target(idxIDs=None, target=None):

    # select sg-part of the target 
    if 'idx_combi' in list(idxIDs.keys()):
        # select right rows from target data
        id_atts = idxIDs['id_atts'] # has length two: IDCode, PreOrd
        seltarget = target[target.set_index(id_atts).index.isin(idxIDs['idx_combi'])] # creates a tuple index, compares with tuples in idxIDs
    else:
        seltarget = target[target[idxIDs['id_atts'][0]].isin(idxIDs['idx_id'])]
    
    return seltarget

def select_bin_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()

    #if sel[0] == 'NaN':
    #    sel_idx = df[df[att].isnull()].index.values
    #else:
    sel_idx = df[df[att] == sel].index.values

    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def select_num_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()

    if sel[0] == 'NaN':
        sel_idx = df[df[att].isnull()].index.values
    else:
        low_idx =  df[df[att] >= sel[0]].index.values # value can be equal to the lower bound
        up_idx = df[df[att] <= sel[1]].index.values # value can be equal to the upper bound            
        sel_idx = np.intersect1d(low_idx, up_idx)
    
    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def select_nom_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()
    tup = sel

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)
  
    # when the first value is a 1, then take all datapoints with the value in position two
    if tup[0] == 1.0:
        df_drop = df[df[att].notnull()]
        sel_idx = df_drop[df_drop[att] == tup[1]].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)
        
    # when the first value is a 0, then take all datapoints that do not have the value in position two
    elif tup[0] == 0.0:
        df_drop = df[df[att].notnull()]
        sel_idx = df_drop[df_drop[att] != tup[1]].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)

    idx_out = idx_in.copy()

    return idx_out    

def select_ord_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()        

    if sel[0] == 'NaN':
        sel_idx = df[df[att].isnull()].index.values
    else:
        # a loop over all categories in the description
        # cases that equal either of the categories should be selected
        sel_idx = df[df[att].isin(sel)].index.values

    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out   