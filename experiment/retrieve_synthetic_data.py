import numpy as np
import pandas as pd
import os

import data_input.synthetic.synthetic_main as ism
    
def retrieve_synthetic_data(data_from=None, synparams=None, datasets_names=None):

    syn_data_at_path = data_from + 'synthetic/data/' + str(list(synparams)) + '/'
    if not os.path.exists(syn_data_at_path):
        os.makedirs(syn_data_at_path)
    
        dfs = ism.generate_synthetic_data(datasets_names=datasets_names, synparams=synparams)
        # store datasets there
        for sheet_name in dfs.keys():
            print(sheet_name)
            dfs[sheet_name].to_parquet(syn_data_at_path + sheet_name + '.pq')
            
    else: 

        # extract data from there    
        dfs = import_synthetic_data(data_from=syn_data_at_path, datasets_names=datasets_names)
        
    descriptive_datasets, attribute_sets, target = prepare_synthetic_data(dict=dfs)

    return descriptive_datasets, attribute_sets, target, syn_data_at_path

def import_synthetic_data(data_from=None, datasets_names=None):

    dict = {}
    for sheet_name in datasets_names:
        dict[sheet_name] = pd.read_parquet(data_from + sheet_name + '.pq')

    dict['target'] = pd.read_parquet(data_from + 'target.pq')
    dict['IDs'] = pd.read_parquet(data_from + 'IDs.pq')

    return dict

def prepare_synthetic_data(dict=None):

    IDs = dict['IDs']['ID'].tolist()
    target = dict['target']
    target.reset_index(inplace=True,drop=True)

    # extract descriptive datasets
    descriptives = {}
    for name in datasets_names:
        data = dict[name]
        keep_cols = data.columns.values
        data = data[keep_cols]
        data.reset_index(inplace=True,drop=True)
        descriptives[name] = data

    attribute_sets = {}
    for key in descriptives.keys():
        types = data.dtypes
        types.drop('IDCode', inplace=True)
        print(types)

        attributes = {'bin_atts': [], 
                      'num_atts': [], 
                      'nom_atts': [], 
                      'ord_atts': []}
        
        if key in ['long_target', 'long']:
            attributes['id_atts'] = ['IDCode','TimeInd']
        else:
            attributes['id_atts'] = ['IDCode']

        attribute_sets[key] = attributes

    return descriptives, attributes, target