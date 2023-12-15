import pandas as pd
import preprocess_data as pp
import preprocess_into_wide as ppw
import preprocess_into_long as ppl
import preprocess_into_desc as ppd

def main(tasks=None, date=None, path_from=None, path_to=None):

    # general preprocess
    descriptive_datasets, target, descriptive_basic, datasets_cases, info, IDs = pp.preprocess_data(tasks=tasks, path_from=path_from)
    info['date'] = date

    # with description models desc
    descriptive_desc, info, descriptive_desc_adapt_to_target = ppd.into_desc(descriptive_datasets, descriptive_basic, info)  

    # into long
    descriptive_long_adapt_to_target, descriptive_long, info = ppl.into_long(descriptive_datasets, descriptive_basic, target, info)    

    # into wide
    descriptive_wide, info, ddwide10, ddwide50, ddwide90, descriptive_wide_adapt_to_target = ppw.into_wide(descriptive_long, descriptive_basic, info)

    print('save as xlsx and pq')
    dfs = descriptive_datasets
    dfs.update({'descriptive_basic': descriptive_basic, 'target': target, 'info': pd.DataFrame(info, index=[0]), 'IDs': pd.DataFrame(IDs,columns=['ID'])})
    
    dfs.update({
        'descriptive_desc': descriptive_desc,
        'descriptive_desc_target': descriptive_desc_adapt_to_target, 
        'descriptive_long': descriptive_long, 
        'descriptive_long_target': descriptive_long_adapt_to_target,
        'descriptive_wide': descriptive_wide,
        'descriptive_wide_10': ddwide10,     
        'descriptive_wide_50': ddwide50,     
        'descriptive_wide_90': ddwide90,     
        'descriptive_wide_target': descriptive_wide_adapt_to_target 
        })
    
    #writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
    for sheet_name in dfs.keys():
        print(sheet_name)
        dfs[sheet_name].to_parquet(path_to + sheet_name + '.pq')
        #dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    #writer.save()

if __name__ == '__main__':

    main(tasks=['NC','SA','SS','CA','DM'],
         date='06112023',
         path_from="C:/Users/20200059/Documents/Data/FUNA/Received/",
         path_to="C:/Users/20200059/Documents/Data/FUNA/DescriptionModels/")
