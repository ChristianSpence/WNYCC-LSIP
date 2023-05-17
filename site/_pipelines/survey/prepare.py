import os
import sys
import pandas as pd
import re
from lookups import LA_CODES


def slugify_column_name(name):
    return re.sub(r'\s+', '_', name).replace('.', '').replace('*', '_star').lower()

def load_data(filepath):
    data = pd.read_excel(filepath)
    return data

if __name__ == '__main__':
    filepath = 'data-raw/lsip-survey/short Survey responses 3-4-23.xlsx'
    data = load_data(filepath) 
                    #  names=['LSIPs: LSIPs Name', 'Chamber', 'Local Authority',
                    #                   'Company Sector', 'Skills Gap', 'Challenge Recruiting', 
                    #                   'Technical Skills', 'Soft Skills', 'Functional Skills', 
                    #                   'Other', 'Access Correct Training', 'Training Format',
                    #                   'Identified Changes in Skills'])
    value_counts = data.value_counts(subset=['Local Authority', 'Skills Gap'])
    df_value_counts = pd.DataFrame(value_counts).sort_index()
    print(df_value_counts)
    
    group = sys.argv[1]
    OUTDIR = 'site/{group}/demand/survey/_data/'.format(group=group)
    os.makedirs(OUTDIR, exist_ok=True)
    df_value_counts = df_value_counts.pivot_table(values='count', index='Local Authority', columns='Skills Gap')
    if group == 'wycc':
        df_value_counts = df_value_counts.drop(['City of York', 'North Yorkshire'])
        df_value_counts.to_csv(os.path.join(OUTDIR, 'skills_gap_by_LA.csv'))
    else:
        df_value_counts = df_value_counts.drop(['Bradford', 'Calderdale', 'Leeds', 'Kirklees', 'Wakefield'])
        df_value_counts.to_csv(os.path.join(OUTDIR, 'skills_gap_by_LA.csv'))
    
    ##need to pivot table for data vis so it works as expected.
    ##can keep other stuff same.