import numpy as np
import pandas as pd
import random
import itertools as it


def retrieve_data_funa(dict=None, datasets_names=None, extra_info=None):

    IDs = dict['IDs']['ID'].tolist()
    target = dict['target']

    sample = extra_info['sample']
    sample_prop = extra_info['sample_prop']

    if sample:
        # for now, select a fixed 5 percent, and only work with NC columns
        random.seed(2024)
        selIDs = random.sample(IDs, int(sample_prop*len(IDs)))
        # print(selIDs[0:10])

        # extract target
        target = target[target['IDCode'].isin(selIDs)]
    target.reset_index(inplace=True, drop=True)

    # extract descriptive datasets
    descriptives = {}
    for name in datasets_names:
        data = dict[name]
        if sample:
            data = data[data['IDCode'].isin(selIDs)].copy()
        # if sample:
        #    cols = data.columns.values
        #    keep_cols =  [col for col in cols if col.startswith('NC')]
        #    keep_cols = keep_cols + ['IDCode','sex','grade','language']
        #    if 'long' in name:
        #        keep_cols.append('PreOrd')
        # else:
        #    keep_cols = list(data.columns.values)
        keep_cols = list(data.columns.values)
        dataset = data[keep_cols].copy()
        dataset['grade'] = dataset['grade'].astype('category')
        dataset.reset_index(inplace=True, drop=True)
        descriptives[name] = dataset

        '''
        if 'desc' == name:
            path_to = "./data_input/FUNA/slice/"
            dataset.to_parquet(path_to + 'desc.pq')
            target.to_parquet(path_to + 'target.pq')
            print('done')
        '''

    # store names of descriptors for each of the descriptive datasets
    attribute_sets = {}
    for key in descriptives.keys():

        # exceptions that can be handled in the data by changing the type
        data = change_type(data=descriptives[key])

        types = data.dtypes
        types.drop('IDCode', inplace=True)

        # exceptions that are handled manually
        attributes = {'bin_atts': [], 'num_atts': [],
                      'nom_atts': [], 'ord_atts': []}
        attributes, types = handle_type_exceptions(
            attributes=attributes, types=types)

        if 'without' in key:  # we do not use PreOrd as a descriptor, only as an id indicator
            types.drop('PreOrd', inplace=True)

        # funa descriptors often run from 1 - 9, we currently consider them as numerical attributes, but may be useful to change this to ordinal in the future

        attributes['bin_atts'] = attributes['bin_atts'] + []
        attributes['num_atts'] = attributes['num_atts'] + list(types[types == 'float64'].index.values) + list(
            types[types == 'int64'].index.values) + list(types[types == 'int32'].index.values)
        attributes['nom_atts'] = attributes['nom_atts'] + \
            list(types[types == 'object'].index.values)
        attributes['ord_atts'] = attributes['ord_atts'] + \
            list(types[types == 'category'].index.values)

        if 'long' in key:
            if 'full_target' in key:
                attributes['id_atts'] = ['IDCode']
            else:
                attributes['id_atts'] = ['IDCode', 'PreOrd']
        else:
            attributes['id_atts'] = ['IDCode']

        attribute_sets[key] = attributes

    return descriptives, attribute_sets, target


def handle_type_exceptions(attributes=None, types=None):

    should_be_seen_as_binary = ['sex', 'language']
    if 'NCAnsC' in types.index.values:
        should_be_seen_as_binary = should_be_seen_as_binary + ['NCAnsC']
    types.drop(should_be_seen_as_binary, inplace=True, errors='ignore')
    attributes['bin_atts'] = should_be_seen_as_binary

    return attributes, types


def change_type(data=None):

    cols = data.columns.values
    if 'NCAns' in cols:
        # cannot change to int since the column may contain missing values
        data['NCAns'] = pd.to_numeric(data['NCAns'], errors='coerce')

    return data


def import_data_funa(data_name=None, data_from=None, datasets_names=None):

    print('importing data')
    # dict = pd.read_excel('prepareData/' + data_name + '/data.xlsx', sheet_name=None) # retrieve as dictionary, takes about an hour
    dict = {}
    for sheet_name in datasets_names:
        if 'long' in sheet_name:
            if 'long_adapt' in sheet_name:
                dict[sheet_name] = pd.read_parquet(
                    data_from + data_name + '/FUNA_EMM/descriptive_' + 'long_adapt' + '.pq')
            else:
                dict[sheet_name] = pd.read_parquet(
                    data_from + data_name + '/FUNA_EMM/descriptive_' + 'long' + '.pq')
        else:
            dict[sheet_name] = pd.read_parquet(
                data_from + data_name + '/FUNA_EMM/descriptive_' + sheet_name + '.pq')

    # import target data, import IDs
    dict['target'] = pd.read_parquet(
        data_from + data_name + '/FUNA_EMM/target.pq')
    dict['IDs'] = pd.read_parquet(data_from + data_name + '/FUNA_EMM/IDs.pq')

    return dict
