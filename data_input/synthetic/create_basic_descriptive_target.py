import pandas as pd
import numpy as np
import string
import random
import matplotlib.pyplot as plt

def create_descriptive(synparams=None):

    random.seed(2024)

    N = synparams[0]
    T = synparams[1]
    G = synparams[2]
    groups = list(string.ascii_lowercase[0:G])

    info = {'N': N, 'T': T, 'G': G, 'groups': groups, 'seed': 2024}

    sampled_groups = random.choices(groups, k=N*T) # this create uniform distribution of cases with equal probability of having one of the G^T possible sequences
    #sampled_groups = np.repeat(random.choices(groups, k=N),T)
    IDs = ['id'+str(i) for i in list(np.repeat(np.arange(1,N+1),T))] 

    descriptive = pd.DataFrame({'IDCode': IDs,
                                'TimeInd': np.tile(np.arange(1,T+1),N),
                                'Group': sampled_groups})
    # group as ordinal variable
    descriptive_ord = transform_group_into_ordinal(descriptive=descriptive)

    return descriptive_ord, info, list(set(IDs))

def transform_group_into_ordinal(descriptive=None):

    descriptive_ord = descriptive.copy()
    
    descriptive_ord['Group'] = descriptive_ord['Group'].astype('category') # will assume that alphabetical order will be maintained

    print(descriptive_ord.dtypes)

    return descriptive_ord

def create_targets(descriptive=None, info=None):

    T = descriptive['TimeInd'].max()

    cat_values = descriptive['Group'].values.categories
    cat_codes = descriptive['Group'].values.codes
    groups_int = np.unique(cat_codes)

    subgroups = define_subgroups(descriptive=descriptive, T=T, groups_int=groups_int, cat_values=cat_values)
    target = descriptive[['IDCode', 'TimeInd', 'Group']].copy()

    for type_subgroup in subgroups.keys(): # 8
        
        target['Target'+type_subgroup] = np.nan
        target['GroupTimeDistance'+type_subgroup] = np.nan

        group_time_distances = subgroups[type_subgroup] #length of T * G
        for t in np.arange(1,T+1):
            for g in groups_int:
                group_time_size = group_time_distances.loc[(t,cat_values[g]), 'IDCount']
                group_time_distance = group_time_distances.loc[(t,cat_values[g]), 'y']
                target_data = np.random.normal(loc=10.0+group_time_distance, scale=0.01, size=group_time_size)
                
                target.loc[(target['TimeInd'] == t) & (target['Group'] == cat_values[g]), 'Target'+type_subgroup] = target_data
                target.loc[(target['TimeInd'] == t) & (target['Group'] == cat_values[g]), 'GroupTimeDistance'+type_subgroup] = np.repeat(group_time_distance, group_time_size)
                
                info.update({type_subgroup+str(t)+cat_values[g]: (group_time_distance, group_time_size)})

    # improvement: scale the subgroup types such that the global average of GroupTimeDistance is 0 and the min-max are the same for every subgroup
        
    # create figure and store figure
    if info['G'] == 5 and info['T'] == 20: 
        create_and_store_subgroup_figures(subgroups=subgroups)
    #if info['G'] == 3 and info['T'] == 3:     
    #    create_and_store_effect_figures(target=target)

    target.drop(['Group', 'GroupTimeDistanceA', 'GroupTimeDistanceB', 'GroupTimeDistanceC', 'GroupTimeDistanceD', 'GroupTimeDistanceE', 'GroupTimeDistanceF', 'GroupTimeDistanceG', 'GroupTimeDistanceH'], axis = 1, inplace=True)

    return target, info

def define_subgroups(descriptive=None, T=None, groups_int=None, cat_values=None):

    subgroups = {}
    for type_subgroup in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        group_time_means = descriptive.copy()
        group_time_means = group_time_means.groupby(['TimeInd', 'Group']).count().unstack(fill_value=0).stack()        
        group_time_means.rename({'IDCode':'IDCount'}, axis='columns', inplace=True)
        group_time_means['y'] = np.nan
        for t in np.arange(1,T+1):
            for g in groups_int:
                group_time_means.loc[(t,cat_values[g]), 'y'] = calculate_subgroup_distance(type_subgroup=type_subgroup, t=t, g=g, T=T, G=len(groups_int)) 
        subgroups.update({type_subgroup: group_time_means})

    return subgroups

def calculate_subgroup_distance(type_subgroup=None, t=None, g=None, T=None, G=None):

    lowest = -3
    highest = 3

    T = T-1
    G = G-1

    x1 = t-1 # time 1 refers to 0 in the linear equation
    x2 = g # group 'a' refers to 0 in the linear equation

    if type_subgroup in ['A', 'B', 'C', 'D']:     
        gamma = 0 # no interaction
        if type_subgroup == 'A':
            step_per_timepoint = 0
            step_per_group = 0
            lowest = 0 # no effect
        if type_subgroup == 'B':
            step_per_timepoint = (highest - lowest) / T
            step_per_group = 0   
        if type_subgroup == 'C':
            step_per_timepoint = 0
            step_per_group = (highest - lowest) / G   
        if type_subgroup == 'D':        
            step_per_timepoint = ((highest - lowest)/2) / T
            step_per_group = ((highest - lowest)/2) / G         
        alpha = step_per_timepoint
        beta = step_per_group
        y = lowest + alpha * x1 + beta * x2 + gamma * x1 * x2
    
    if type_subgroup in ['E', 'F', 'G', 'H']:
        if type_subgroup == 'E':
            start_line = lowest + x2*((highest - lowest) / G)
            end_line = highest - x2*((highest - lowest) / G)
            slope = (end_line - start_line) / T
        if type_subgroup == 'F':
            start_line = lowest + x2*(((highest-lowest)/2) / G)
            end_line = highest - x2*(((highest-lowest)/2) / G)
            slope = (end_line - start_line) / T        
        if type_subgroup == 'G':
            start_line = lowest + x2*((highest-lowest) / G)
            end_line = lowest + (highest-lowest)/2
            slope = (end_line - start_line) / T        
        if type_subgroup == 'H':
            start_line = lowest
            end_line = highest - x2*(((highest-lowest)/2) / G)
            slope = (end_line - start_line) / T      
        y = start_line + x1 * slope       
        
    return y

def create_and_store_subgroup_figures(subgroups=None):
    
    for type_subgroup in subgroups.keys(): # 8

        group_time_means = subgroups[type_subgroup] #length of T * G
        gtm = group_time_means.reset_index()
        groups = gtm.groupby('Group')

        fig, ax = plt.subplots()    
        for name, group in groups:
            ax.plot(group.TimeInd, group.y, marker='o', linestyle='', ms=6, label=name)
            ax.legend()
        plt.title('Extent of exceptionality for subgroup type ' + type_subgroup)
        plt.xlabel('TimeInd')
        plt.ylabel('Distance of target value to global')
        plt.grid(True)       
    
        plt.savefig("data_input/synthetic/figures/" + "ExceptionalityType"+type_subgroup+".pdf", format="pdf", bbox_inches="tight")
        #plt.show()

def create_and_store_effect_figures(target=None):

    subgroups = ['A', 'B', 'C', 'D'] + ['E', 'F', 'G', 'H']    

    for type_subgroup in subgroups: # 8

        df = target[['IDCode', 'TimeInd', 'Group', 'GroupTimeDistance'+type_subgroup]].copy()
        df.rename({'GroupTimeDistance'+type_subgroup : 'GroupTimeDistance'}, axis='columns', inplace=True)
    
        seldf5 = df[df.IDCode.isin(random.sample(list(df.IDCode.unique()), 5))]
        groups = seldf5.groupby('IDCode')
        fig, ax = plt.subplots()
        ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
        for name, group in groups:
            ax.plot(group.TimeInd, group.GroupTimeDistance, marker='o', linestyle='-', ms=2, label=name)
        ax.legend()
        plt.title('Example of possible distances per case per timepoint for subgroup type ' + type_subgroup)
        plt.xlabel('TimeInd')
        plt.ylabel('Distance of target value to global')
        plt.grid(True)
        plt.savefig("data_input/synthetic/figures/" + "ExampleGroupTimeDistance"+type_subgroup+".pdf", format="pdf", bbox_inches="tight")       
        #plt.show()
    
        seldf100 = df[df.IDCode.isin(random.sample(list(df.IDCode.unique()), 1000))]
        seqs = seldf100.groupby('IDCode').agg({'Group':lambda x: ''.join(x), 
                                               'GroupTimeDistance':'sum'}).reset_index()
        seqs = seqs.sort_values('Group')
        
        '''
        fig = plt.figure()
        plt.hist(seqs['Group'])
        plt.xticks(rotation=90)
        plt.title('')
        plt.xlabel('Sequence of groups over timepoints')
        plt.ylabel('Number of cases')
        plt.show()
        '''

        fig = plt.figure()
        plt.plot(seqs.Group, seqs.GroupTimeDistance, marker='o', linestyle='-', ms=2)
        plt.xticks(rotation=90)
        plt.title('Average of total distance per case for subgroup type ' + type_subgroup)
        plt.xlabel('Sequence of groups over timepoints')
        plt.ylabel('Distance of target value to global')
        plt.grid(True) 
        plt.savefig("data_input/synthetic/figures/" + "AverageSumGroupTimeDistance"+type_subgroup+".pdf", format="pdf", bbox_inches="tight")       
        #plt.show()
    

