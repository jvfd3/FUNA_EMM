import pandas as pd

def result_set_to_df(result_set=None):

    result_emm = pd.DataFrame

    if len(result_set) > 0:

        #print(result_set[0].keys()) # description, adds, qualities  
        # adds: literal_order, idxIDs
        # qualities: estimates, varphi

        descs_result_set_dict = {sg: desc['description'] for sg, desc in enumerate(result_set)}
        descs_pd = pd.DataFrame.from_dict(descs_result_set_dict, orient='index')

        results_pd = obtain_subgroup_results(result_set=result_set)
        result_emm = pd.concat((descs_pd,results_pd),axis=1)        

    return result_emm

def obtain_subgroup_results(result_set=None):

    subgroup_results = [(desc['adds']['literal_order'],
                         desc['qualities']['varphi'],
                         desc['adds']['idxIDs']['size_sg'],
                         desc['adds']['idxIDs']['size_sg_rows'],
                         desc['adds']['idxIDs']['idx_id'], # will remove these later when saving the result set
                         desc['adds']['idxIDs']['idx_sg']) # will remove these later when saving the result set
                         
                         for desc in result_set]

    subgroup_results_pd = pd.DataFrame(subgroup_results, 
                                       columns= ['literal_order',
                                                 'varphi',
                                                 'size_id',
                                                 'size_rows',
                                                 'idx_id',
                                                 'idx_sg'])

    dfall = pd.DataFrame()
    for desc in result_set:
        dictdesc = desc['qualities']['estimates']
        df = pd.Series(dictdesc).to_frame()
        dfall = pd.concat((dfall,df),axis=1)
    
    subgroup_results_pd = pd.concat((subgroup_results_pd,dfall.T.reset_index(drop=True)),axis=1)
    #print(subgroup_results_pd)
    
    return subgroup_results_pd