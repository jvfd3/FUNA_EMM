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

    sampled_groups = random.choices(groups, k=N*T)
    IDs = ['id'+str(i) for i in list(np.repeat(np.arange(1,N+1),T))] 

    descriptive = pd.DataFrame({'IDCode': IDs,
                                'TimeInd': np.tile(np.arange(1,T+1),N),
                                'Group': sampled_groups})

    return descriptive, info, list(set(IDs))

def create_targets(descriptive=None, info=None):

    T = descriptive['TimeInd'].max()
    groups = list(descriptive['Group'].unique())

    subgroups = define_subgroups(descriptive=descriptive, T=T, groups=groups)
    target = descriptive[['IDCode', 'TimeInd', 'Group']].copy()

    for type_subgroup in subgroups.keys(): # 8
        
        target['Target'+type_subgroup] = np.nan
        group_time_means = subgroups[type_subgroup] #length of T * G
        for t in np.arange(1,T+1):
            for g in groups:
                group_time_size = group_time_means.loc[(t,g), 'IDCount']
                group_time_mean = group_time_means.loc[(t,g), 'y']
                target_data = np.random.normal(loc=10.0+group_time_mean, scale=1.0, size=group_time_size)
                
                target.loc[(target['TimeInd'] == t) & (target['Group'] == g), 'Target'+type_subgroup] = target_data
                info.update({type_subgroup+str(t)+g: (group_time_mean, group_time_size)})
        
    target.drop(['Group'], axis = 1, inplace=True)

    # create figure and store figure
    #figs = create_and_store_figure(subgroups=subgroups)

    return target, info

def define_subgroups(descriptive=None, T=None, groups=None):

    subgroups = {}
    for type_subgroup in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        group_time_means = descriptive.copy()
        group_time_means = group_time_means.groupby(['TimeInd', 'Group']).count().unstack(fill_value=0).stack()        
        group_time_means.rename({'IDCode':'IDCount'}, axis='columns', inplace=True)
        group_time_means['y'] = np.nan
        for t in np.arange(1,T+1):
            for g in groups:
                group_time_means.loc[(t,g), 'y'] = calculate_subgroup_distance(type_subgroup=type_subgroup, t=t, g=g, T=T, G=len(groups)) 
        subgroups.update({type_subgroup: group_time_means})

    return subgroups

def calculate_subgroup_distance(type_subgroup=None, t=None, g=None, T=None, G=None):

    lowest = -3
    highest = 3

    T = T-1
    G = G-1

    x1 = t-1 # time 1 refers to 0 in the linear equation
    x2 = string.ascii_lowercase.index(g) # group 'a' refers to 0 in the linear equation

    if type_subgroup in ['B', 'E', 'F', 'G']: 
        gamma = 0 # no interaction
        if type_subgroup == 'B':        
            step_per_timepoint = ((highest - lowest)/2) / T
            step_per_group = ((highest - lowest)/2) / G
        if type_subgroup == 'E':
            step_per_timepoint = (highest - lowest) / T
            step_per_group = 0
        if type_subgroup == 'F':
            step_per_timepoint = 0
            step_per_group = 0
            lowest = 0 # no effect
        if type_subgroup == 'G':
            step_per_timepoint = 0
            step_per_group = (highest - lowest) / G            
        alpha = step_per_timepoint
        beta = step_per_group
        y = lowest + alpha * x1 + beta * x2 + gamma * x1 * x2
    
    if type_subgroup in ['A', 'C', 'D', 'H']:
        if type_subgroup == 'A':
            start_line = lowest + x2*((highest - lowest) / G)
            end_line = highest - x2*((highest - lowest) / G)
            slope = (end_line - start_line) / T
        if type_subgroup == 'C':
            start_line = lowest + x2*(((highest-lowest)/2) / G)
            end_line = highest - x2*(((highest-lowest)/2) / G)
            slope = (end_line - start_line) / T
        if type_subgroup == 'D':
            start_line = lowest
            end_line = highest - x2*(((highest-lowest)/2) / G)
            slope = (end_line - start_line) / T
        if type_subgroup == 'H':
            start_line = lowest + x2*((highest-lowest) / G)
            end_line = lowest + (highest-lowest)/2
            slope = (end_line - start_line) / T
        y = start_line + x1 * slope       
        
    return y

def create_and_store_figure(subgroups=None):

    figs = {}

    for type_subgroup in subgroups.keys(): # 8
        group_time_means = subgroups[type_subgroup] #length of T * G
        gtm = group_time_means.reset_index()
        groups = gtm.groupby('Group')

        fig, ax = plt.subplots()
        ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
        for name, group in groups:
            ax.plot(group.TimeInd, group.y, marker='o', linestyle='', ms=6, label=name)
        ax.legend()
        plt.title('Extent of exceptionality for subgroup type ' + type_subgroup)
        plt.xlabel('TimeInd')
        plt.ylabel('Distance of target value')
        plt.grid(True)       
        plt.show()

    return figs
    

