import numpy as np
import pandas as pd


def retrieve_data_curran(dict=None, datasets_names=None):

    target = dict['target']
    target.reset_index(inplace=True, drop=True)

    descriptives = {}
    for name in datasets_names:
        dataset = dict[name]
        if 'long' in name:
            dataset['occasion'] = dataset['occasion'].astype('category')
        dataset.reset_index(inplace=True, drop=True)
        descriptives[name] = dataset

    attribute_sets = {}
    for key in descriptives.keys():

        data = descriptives[key]
        types = data.dtypes
        types.drop('id', inplace=True)

        # exceptions that are handled manually
        attributes = {'bin_atts': [], 'num_atts': [],
                      'nom_atts': [], 'ord_atts': []}
        attributes, types = handle_type_exceptions(
            attributes=attributes, types=types)

        if 'without' in key:  # we do not use PreOrd as a descriptor, only as an id indicator
            types.drop('occasion', inplace=True)

        attributes['bin_atts'] = attributes['bin_atts'] + []
        attributes['num_atts'] = attributes['num_atts'] + list(types[types == 'float64'].index.values) + list(
            types[types == 'int64'].index.values) + list(types[types == 'int32'].index.values)
        attributes['nom_atts'] = attributes['nom_atts'] + \
            list(types[types == 'object'].index.values)
        attributes['ord_atts'] = attributes['ord_atts'] + \
            list(types[types == 'category'].index.values)

        if 'long' in key:
            attributes['id_atts'] = ['id', 'occasion']
        else:
            attributes['id_atts'] = ['id']

        attribute_sets[key] = attributes

    return descriptives, attribute_sets, target


def handle_type_exceptions(attributes=None, types=None):

    should_be_seen_as_binary = ['kidgen']
    types.drop(should_be_seen_as_binary, inplace=True, errors='ignore')
    attributes['bin_atts'] = should_be_seen_as_binary

    return attributes, types


def import_data_curran(data_name=None, data_from=None, datasets_names=None):

    print('importing data')
    dict = {}
    for sheet_name in datasets_names:
        if 'long' in sheet_name:
            dict[sheet_name] = pd.read_parquet(
                data_from + data_name + '/data/long.pq')
        else:
            dict[sheet_name] = pd.read_parquet(
                data_from + data_name + '/data/' + sheet_name + '.pq')

    # import target data, import IDs
    dict['target'] = pd.read_parquet(data_from + data_name + '/data/target.pq')

    return dict
