import numpy as np
import itertools as it

import beam_search.refinements_functions as rff


def create_starting_descriptions(descriptive=None, attributes=None, b=None, md=None):

    # should start with binary attributes!
    cq_bin = refine_binary_attributes(
        seed=None, dataset=descriptive, subgroup=None, binary_attributes=attributes['bin_atts'], md=md)

    cq_bin_nom = refine_nominal_attributes(
        cq=cq_bin, seed=None, dataset=descriptive, subgroup=None, nominal_attributes=attributes['nom_atts'], md=md)

    cq_bin_nom_num = refine_numerical_attributes(
        cq=cq_bin_nom, seed=None, dataset=descriptive, subgroup=None, numerical_attributes=attributes['num_atts'], b=b, md=md)

    cq_bin_nom_num_ord = refine_ordinal_attributes(
        cq=cq_bin_nom_num, seed=None, dataset=descriptive, subgroup=None, ordinal_attributes=attributes['ord_atts'], md=md)

    return cq_bin_nom_num_ord


def refine_seed(seed=None, subgroup=None, attributes=None, md=None, b=None):

    # should start with binary attributes!
    cq_bin = refine_binary_attributes(
        seed=seed, dataset=None, subgroup=subgroup, binary_attributes=attributes['bin_atts'], md=md)

    cq_bin_nom = refine_nominal_attributes(
        cq=cq_bin, seed=seed, dataset=None, subgroup=subgroup, nominal_attributes=attributes['nom_atts'], md=md)

    cq_bin_nom_num = refine_numerical_attributes(
        cq=cq_bin_nom, seed=seed, dataset=None, subgroup=subgroup, numerical_attributes=attributes['num_atts'], b=b, md=md)

    cq_bin_nom_num_ord = refine_ordinal_attributes(
        cq=cq_bin_nom_num, seed=seed, dataset=None, subgroup=subgroup, ordinal_attributes=attributes['ord_atts'], md=md)

    return cq_bin_nom_num_ord


def refine_binary_attributes(seed=None, dataset=None, subgroup=None,
                             binary_attributes=None, md=None):

    refined_cq = []

    # first candidate queue
    if seed is None:

        for attribute in binary_attributes:

            new_descriptions = rff.make_descriptions(
                dataset=dataset, attribute=attribute, type_desc='bin', md=md)
            refined_cq = refined_cq + new_descriptions

    # refinements for a seed
    else:

        description = seed['description']
        lit = seed['adds']['literal_order']

        for attribute in binary_attributes:
            if not attribute in list(description.keys()):

                add_refinements = rff.make_descriptions(
                    dataset=subgroup, attribute=attribute, type_desc='bin', md=md)
                new_descriptions = rff.concatenate_literals(
                    description=description, lit=lit, add_refinements=add_refinements)
                refined_cq = refined_cq + new_descriptions

    return refined_cq


def refine_nominal_attributes(cq=None, seed=None, dataset=None, subgroup=None,
                              nominal_attributes=None, md=None):

    refined_cq = cq

    # first candidate queue
    if seed is None:

        for attribute in nominal_attributes:

            new_descriptions = rff.make_descriptions(
                dataset=dataset, attribute=attribute, type_desc='nom', md=md)
            refined_cq = refined_cq + new_descriptions

    # refinements for a seed
    else:

        description = seed['description']
        lit = seed['adds']['literal_order']

        for attribute in nominal_attributes:
            if not attribute in list(description.keys()):

                add_refinements = rff.make_descriptions(
                    dataset=subgroup, attribute=attribute, type_desc='nom', md=md)
                new_descriptions = rff.concatenate_literals(
                    description=description, lit=lit, add_refinements=add_refinements)
                refined_cq = refined_cq + new_descriptions

                '''
                if any(subgroup[attribute].isnull()):                
                    temp_desc = description.copy()
                    temp_desc[attribute] = ['NaN']
                    refined_cq.append({'description' : temp_desc, 
                                       'adds': {'literal_order' : lit + (attribute,)}})
                '''

    return refined_cq


def refine_numerical_attributes(cq=None, seed=None, dataset=None, subgroup=None, numerical_attributes=None, b=None, md=None):

    refined_cq = cq

    # first candidate queue
    if seed is None:
        for attribute in numerical_attributes:

            new_descriptions = rff.make_descriptions(
                dataset=dataset, attribute=attribute, type_desc='num', md=md, b=b)
            refined_cq = refined_cq + new_descriptions

    # refinements for a seed
    else:

        description = seed['description']
        lit = seed['adds']['literal_order']

        for attribute in numerical_attributes:  # existing attributes will be replaced

            add_refinements = rff.make_descriptions(
                dataset=subgroup, attribute=attribute, type_desc='num', md=md, b=b)
            new_descriptions = rff.concatenate_literals(
                description=description, lit=lit, add_refinements=add_refinements)
            refined_cq = refined_cq + new_descriptions

    return refined_cq


def refine_ordinal_attributes(cq=None, seed=None, dataset=None, subgroup=None,
                              ordinal_attributes=None, md=None):

    refined_cq = cq

    # first candidate queue
    if seed is None:
        for attribute in ordinal_attributes:

            new_descriptions = rff.make_descriptions(
                dataset=dataset, attribute=attribute, type_desc='ord', md=md)
            refined_cq = refined_cq + new_descriptions

    # refinements for a seed
    else:
        description = seed['description']
        lit = seed['adds']['literal_order']

        for attribute in ordinal_attributes:

            # every possible subsequence will be checked, therefore not necessary to check again
            if not attribute in list(description.keys()):

                add_refinements = rff.make_descriptions(
                    dataset=subgroup, attribute=attribute, type_desc='ord', md=md)
                new_descriptions = rff.concatenate_literals(
                    description=description, lit=lit, add_refinements=add_refinements)
                refined_cq = refined_cq + new_descriptions

    return refined_cq
