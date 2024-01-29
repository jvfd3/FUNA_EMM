import numpy as np
import pandas as pd
import os
import copy

import data_input.synthetic.synthetic_main as ism
    
def retrieve_synthetic_data(data_from=None, synparams=None, datasets_names=None):

    syn_data_at_path = data_from + 'synthetic/data/' + str(list(synparams)) + '/'
    if not os.path.exists(syn_data_at_path):
        os.makedirs(syn_data_at_path)
    
        dfs = ism.generate_synthetic_data(synparams=synparams)
        # store datasets there
        for sheet_name in dfs.keys():
            dfs[sheet_name].to_parquet(syn_data_at_path + sheet_name + '.pq')

        writer = pd.ExcelWriter(syn_data_at_path + 'data.xlsx', engine='xlsxwriter')
        for sheet_name in dfs.keys():
            dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
        writer.close()
            
    else: 

        # extract data from there    
        dfs = import_synthetic_data(data_from=syn_data_at_path, datasets_names=datasets_names)

    descriptive_datasets, attribute_sets, target = prepare_synthetic_data(dict=dfs, datasets_names=datasets_names)

    return descriptive_datasets, attribute_sets, target, syn_data_at_path

def import_synthetic_data(data_from=None, datasets_names=None):

    dict = {}
    for sheet_name in datasets_names:
        if "long" in sheet_name:
            #dict['long_target'] = pd.read_parquet(data_from + 'long_target' + '.pq')
            dict['long_adapt'] = pd.read_parquet(data_from + 'long_adapt' + '.pq')
        elif "desc" in sheet_name:
            #dict['desc_target'] = pd.read_parquet(data_from + 'desc_target' + '.pq')
            dict['desc_adapt'] = pd.read_parquet(data_from + 'desc_adapt' + '.pq')
        elif sheet_name in ['wide_adapt']: 
            dict[sheet_name] = pd.read_parquet(data_from + sheet_name + '.pq')

    dict['target'] = pd.read_parquet(data_from + 'target.pq')
    dict['IDs'] = pd.read_parquet(data_from + 'IDs.pq')

    return dict

def adapt_desc_target_for_subgroup_type(subgroup_type=None, target=None, descriptive_datasets=None, attribute_sets=None):

    targettype = target.copy()
    descriptive_datasetstype = copy.deepcopy(descriptive_datasets) # deepcopy needed because of nesting
    attribute_setstype = copy.deepcopy(attribute_sets) # deepcopy needed because of nesting

    SGTypes_todrop = ['A', 'B', 'C', 'D'] + ['E', 'F', 'G', 'H']
    SGTypes_todrop.remove(subgroup_type)

    # target    
    target_cols_todrop = ['Target'+sg for sg in SGTypes_todrop]
    targettype.drop(columns=target_cols_todrop,axis=1, inplace=True)
    targettype.rename({'Target'+subgroup_type:'Target'},axis=1,inplace=True)

    # descriptive, only needs to be adapted for desc_target_perfect
    if 'desc_adapt_perfect' in list(descriptive_datasets.keys()):
        temp_desc = descriptive_datasetstype['desc_adapt_perfect']
        atts_num = attribute_setstype['desc_adapt_perfect']['num_atts']
        
        descriptors_todrop = ['sum'+sg for sg in SGTypes_todrop] + ['dif'+sg for sg in SGTypes_todrop]    

        temp_desc.drop(columns=descriptors_todrop,axis=1,inplace=True)
        descriptive_datasetstype['desc_adapt_perfect'] = temp_desc
        
        keep_atts_num = [i for i in atts_num if i not in descriptors_todrop]
        attribute_setstype['desc_adapt_perfect']['num_atts'] = keep_atts_num

    return targettype, descriptive_datasetstype, attribute_setstype

def prepare_synthetic_data(dict=None, datasets_names=None):

    IDs = dict['IDs']['ID'].tolist()
    target = dict['target']
    target.reset_index(inplace=True,drop=True)

    # extract descriptive datasets
    descriptives = {}
    for name in datasets_names:
        if "long"in name: # in ['long_target_without', 'long_target_with']:
            data = dict['long_target']
            keep_cols = data.columns.values
        elif "desc" in name: #in ['desc_target_perfect', 'desc_target_medium']:
            data = dict['desc_target']
            keep_cols = data.columns.values
            if name == 'desc_target_perfect':
                idxletters = [i for i in keep_cols if i.startswith('idx')]
                freqletters = [i for i in keep_cols if i.startswith('freq')]
                unwanted_cols = idxletters + freqletters
                keep_cols = [ele for ele in keep_cols if ele not in unwanted_cols]
            elif name == 'desc_target_medium':
                sumgroups = [i for i in keep_cols if i.startswith('sum')]
                difgroups = [i for i in keep_cols if i.startswith('dif')]
                unwanted_cols = sumgroups + difgroups
                keep_cols = [ele for ele in keep_cols if ele not in unwanted_cols]
        else:
            data = dict[name]
            keep_cols = data.columns.values        
        data = data[keep_cols]
        data.reset_index(inplace=True,drop=True)
        descriptives[name] = data

    attribute_sets = {}
    for key in descriptives.keys():
        data = descriptives[key]
        types = data.dtypes
        types.drop('IDCode', inplace=True)

        # exceptions that are handled manually
        attributes = {'bin_atts': [], 'num_atts': [], 'nom_atts': [], 'ord_atts': []}
        attributes, types = handle_type_exceptions(attributes=attributes, types=types, key=key)

        if key == 'long_target_without': # we do not use TimeInd as a descriptor, only as an id indicator
            types.drop('TimeInd', inplace=True)

        attributes['bin_atts'] = attributes['bin_atts'] + []
        attributes['num_atts'] = attributes['num_atts'] + list(types[types == 'float64'].index.values) + list(types[types == 'int64'].index.values) + list(types[types == 'int32'].index.values)
        attributes['nom_atts'] = attributes['nom_atts'] + list(types[types == 'object'].index.values)
        attributes['ord_atts'] = attributes['ord_atts'] + list(types[types == 'category'].index.values)

        if "long" in key: # in ['long_target_with', 'long_target_without']:
            attributes['id_atts'] = ['IDCode','TimeInd']
        else:
            attributes['id_atts'] = ['IDCode']

        attribute_sets[key] = attributes

    return descriptives, attribute_sets, target

def handle_type_exceptions(attributes=None, types=None, key=None):

    should_be_seen_as_binary_invar = [i for i in types.index.values if i.startswith('bininvar')]

    if key in ['long_target_with', 'long_target_without', 'wide_target']:
        should_be_seen_as_binary_var = [i for i in types.index.values if i.startswith('binvar')]
    else:
        should_be_seen_as_binary_var = []    

    should_be_seen_as_binary = should_be_seen_as_binary_invar + should_be_seen_as_binary_var

    types.drop(should_be_seen_as_binary, inplace=True, errors='ignore')
    attributes['bin_atts'] = should_be_seen_as_binary

    return attributes, types