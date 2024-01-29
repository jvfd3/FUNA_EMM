import pandas as pd
import preprocess_functions as pf

def preprocess_data(tasks=None, path_from=None):

    i = 0
    datasets = {}
    datasets_cases = {}
    info = {}
    dataDMs = pd.DataFrame()
    for name_task in tasks:

        print(name_task)
        if name_task != 'DM':
        
            # descriptive data
            data = import_data(name_task=name_task, path_from=path_from)
            data = drop_columns(name_task=name_task, data=data)
            data, IDs_no_correct, data_add_case = drop_cases_with_no_correct(name_task=name_task, data=data)
            data = create_additional_columns_per_item(data=data, name_task=name_task)

            info[name_task + '_IDs_no_correct'] = len(IDs_no_correct)
            datasets[name_task] = data # dictionary
            datasets_cases[name_task] = data_add_case

        # target 
        if name_task == 'DM':

            data = import_data(name_task=name_task, path_from=path_from)
            dataDMs = data.groupby('IDCode').apply(pf.check_suitable_as_target)
            dataDMs.reset_index(drop=True, inplace=True)
            info[name_task + 'IDCodeDMPreOrd'] = dataDMs[['IDCode','DMPreOrd']].copy()
            # add column with item numbers
            #dataDMs = pf.find_max_and_expand(dataDMs) 
            
        i += 1
   
    print('add basic descriptors')  
    only_basic_descriptors = add_descriptor_information(dataDMs=dataDMs)     

    print('remove rows')
    dataDMs, only_basic_descriptors, remy, reme = remove_rows(dataDMs=dataDMs, only_basic_descriptors=only_basic_descriptors)
    info['remy'] = remy 
    info['reme'] = reme 

    print('check and remove IDs')    
    datasets, dataDMs, only_basic_descriptors, IDs = check_IDs(lsdata=datasets, dataDMs=dataDMs, only_basic_descriptors=only_basic_descriptors)  
    info['lenIDs'] = len(IDs)

    print(dataDMs)
    print(dataDMs.shape)

    return datasets, dataDMs, only_basic_descriptors, datasets_cases, info, IDs
    
def import_data(name_task=None, path_from=None):

    #path_file = path_to_data + 'FUNA ExceptionalModelMiningData2021_Subset ' + name_task + '.txt'
    path_file = path_from + 'FUNA ExceptionalModelMiningData2021 ' + name_task + '.txt'
    data = pd.read_csv(path_file, sep='\t', header=0)

    return data 

def drop_columns(name_task=None, data=None):

    if name_task in ['NC','DM']:
        columns_to_drop = [name_task + 'Start', name_task + 'End']
    elif name_task in ['SA','SS','CA']:
        columns_to_drop = [name_task + 'start', name_task + 'end']
    columns_to_drop = columns_to_drop + ['CourseName', 'TeacherIDCode', name_task + 'Cycle']

    data = data.drop(columns_to_drop, axis=1)

    return data

def drop_cases_with_no_correct(name_task=None, data=None):

    data_add_cases = data.groupby('IDCode').apply(pf.check_correct, name_task=name_task)

    IDs_no_correct = list(data_add_cases.index[data_add_cases[name_task + 'AnsCprop'] < 0.05])
    data = data[~data.IDCode.isin(IDs_no_correct)]

    return data, IDs_no_correct, data_add_cases

def create_additional_columns_per_item(data=None, name_task=None):

    data[name_task + 'NumDis'] = (data[name_task + 'StimR'] - data[name_task + 'StimL']).abs()
    data[name_task + 'NumRatio'] = (data[name_task + 'StimR'] - data[name_task + 'StimL']).abs() / data[[name_task + 'StimR', name_task + 'StimL']].max(axis=1)

    return data

def add_descriptor_information(dataDMs=None):

    # we add grade, language, sex to the target data
    basic_descriptors = dataDMs['IDCode'].apply(pf.retrieve_basic_descriptor_information)

    return basic_descriptors

def remove_rows(dataDMs=None, only_basic_descriptors=None):

    # temporary merge between target data and basic descriptors
    target_basic = pd.merge(dataDMs, only_basic_descriptors, left_index=True, right_index=True, suffixes=(None,'_y')) # merge using row index, since IDCode is not unique per row 
    target_basic.drop(target_basic.filter(regex='_y$').columns, axis=1, inplace=True)
    
    # we remove cases that do not follow the requirements
    remy = len(target_basic[target_basic.grade == 'y'])
    reme = len(target_basic[target_basic.language == 'e'])
    
    target_basic = target_basic[(target_basic.grade != 'y') & (target_basic.language != 'e')]

    dataDMs = target_basic[dataDMs.columns.values.tolist()].copy()
    only_basic_descriptors = target_basic[only_basic_descriptors.columns.values.tolist()].copy()

    return dataDMs, only_basic_descriptors, remy, reme

def check_IDs(lsdata=None, dataDMs=None, only_basic_descriptors=None):

    # we check the unique list of IDs in the target data
    targetIDs = list(dataDMs['IDCode'].unique())
    
    # and keep only those IDs that have values in all other tasks
    allIDs = [set(targetIDs)]
    for key in lsdata.keys():
        data = lsdata[key]
        IDs = set(list(data['IDCode'].unique()))
        allIDs.append(IDs)
    
    basicIDs = list(only_basic_descriptors['IDCode'].unique())
    allIDs.append(set(basicIDs))
    intersectionIDs = list(set.intersection(*allIDs))

    dataDMSchecked = dataDMs[dataDMs['IDCode'].isin(intersectionIDs)]
    only_basic_descriptors_checked = only_basic_descriptors[only_basic_descriptors['IDCode'].isin(intersectionIDs)] 
    
    lsdatachecked = {}
    for key in lsdata.keys():
        data = lsdata[key]
        datachecked = data[data['IDCode'].isin(intersectionIDs)]
        lsdatachecked[key] = datachecked

    return lsdatachecked, dataDMSchecked, only_basic_descriptors_checked, intersectionIDs

