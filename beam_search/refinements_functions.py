import numpy as np

def make_descriptions(dataset=None, attribute=None, type_desc=None, md=None, b=None):
     
    new_descriptions = []

    add_refinements = make_literals(dataset=dataset, attribute=attribute, type_desc=type_desc, md=md, b=b)

    # add a part that tracks the order of the literals
    for refinement in add_refinements:
        new_descriptions.append({'description': refinement, 'adds': {'literal_order' : (attribute,)}})
    
    return new_descriptions

def make_literals(dataset=None, attribute=None, type_desc=None, md=None, b=None):

    add_refinements = []
    if type_desc in ['bin','nom']:
        values = dataset.loc[dataset[attribute].notnull(),attribute].unique() 
        for i in range(len(values)):
    
            value = values[i]
            list_of_lits = make_literals_per_type(attribute=attribute, value=value, type_desc=type_desc)
            add_refinements = add_refinements + list_of_lits

    elif type_desc == 'num':
        values = dataset.loc[dataset[attribute].notnull(),attribute]
        quantiles = np.linspace(0, 1, b+1)[1:-1] # for b=4 quantiles, this results in 0.25, 0.5, 0.75
        min_value = values.quantile(0.0) 
        max_value = values.quantile(1.0)
              
        for i in range(b-1):
            value = values.quantile(quantiles[i], interpolation='linear')
            list_of_lits = make_literals_per_type(attribute=attribute, value=value, type_desc=type_desc, min_value=min_value, max_value=max_value)
            add_refinements= add_refinements + list_of_lits

    elif type_desc == 'ord':
        cat_values = dataset[attribute].values.categories
        for i in range(len(cat_values)-1):
            list_of_lits = make_literals_per_type(attribute=attribute, value=i, type_desc=type_desc, values_to_use=cat_values)
            add_refinements= add_refinements + list_of_lits          

    # add md literals in case of md approach (separate)
    if any(dataset[attribute].isnull()): 
        add_refinements = apply_md_approach(md=md, add_refinements=add_refinements, attribute=attribute)

    return add_refinements

def apply_md_approach(md=None, add_refinements=None, attribute=None):

    if md == 'separate': # for every attribute an extra literal
        add_refinements.append({attribute: ['NaN']})
    #if md == 'knn': solved earlier in beam search
    #if md == 'without': influences selection in ss
    #if md == 'included': # needs to be created, either in ss or here
    
    return add_refinements

def concatenate_literals(description=None, lit=None, add_refinements=None): 

    new_descriptions = []
    for refinement in add_refinements:
        temp_desc = description.copy()
        refinement_desc = refinement['description']
        # in case of numerical attributes, check if new values are not the same as old values
        if list(refinement_desc.keys())[0] in list(temp_desc.keys()):
            if refinement_desc[list(refinement_desc.keys())[0]] == temp_desc[list(refinement_desc.keys())[0]]:
                continue
            pass
        temp_desc.update(refinement_desc) # existing key will be overwritten
        new_descriptions.append({'description': temp_desc, 'adds': {'literal_order': lit + (list(refinement_desc.keys())[0],)}})

    return new_descriptions

def make_literals_per_type(attribute=None, value=None, type_desc=None, min_value=None, max_value=None, values_to_use=None):

    list_of_lits = []
    if type_desc == 'bin':
        lit = {attribute: value}
        list_of_lits.append(lit)
    
    if type_desc == 'nom':
        lit = {attribute : (0.0, value)}
        list_of_lits.append(lit)

        lit = {attribute : (1.0, value)}
        list_of_lits.append(lit)

    if type_desc == 'num':
        lit = {attribute : (min_value, value)}
        list_of_lits.append(lit)

        lit = {attribute : (value, max_value)}
        list_of_lits.append(lit)

    if type_desc == 'ord':
        lit = {attribute: list(values_to_use[0:value+1])}
        list_of_lits.append(lit)
        
        lit = {attribute: list(values_to_use[value+1:])}
        list_of_lits.append(lit)
    
    return list_of_lits