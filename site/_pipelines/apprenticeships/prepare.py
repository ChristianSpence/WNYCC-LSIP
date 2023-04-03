import os
import sys
import pandas as pd
import re
from lookups import LA_CODES
from util import slugify, load_data, drop_totals

if __name__ == '__main__':
    filepath = 'data/csv/apprenticeships/apprenticeship_starts_achievements_2022_23.csv'
    group = sys.argv[1]
    OUTDIR = 'site/{group}/supply/apprenticeships/_data/'.format(group=group)
    os.makedirs(OUTDIR, exist_ok=True)

    data = load_data(filepath, group=group, fill_na=False)
    
    #filter by date, only count aggregated numbers for subject, remove aggregates for apprenticeship level. drop useless columns.
    dat = '2022/23'
    data = data[data.date == dat].drop(columns='date')
    all_subjects = data[data.ssa_t1_desc == 'Total'].drop(columns='ssa_t1_desc')
    all_subjects = all_subjects[all_subjects.apprenticeship_level != 'Total']
    all_subjects = all_subjects.set_index('geography_code')
    
    #@TODO need to deal with "low" values for this set of data.
    all_apprenticeship_level = data[data.apprenticeship_level == 'Total'].drop(columns='apprenticeship_level')
    all_apprenticeship_level = all_apprenticeship_level[all_apprenticeship_level.ssa_t1_desc != 'Total']
    all_apprenticeship_level = all_apprenticeship_level.set_index('geography_code')

    total_total = data[(data.ssa_t1_desc == 'Total') & (data.apprenticeship_level == 'Total')].drop(columns=['ssa_t1_desc', 'apprenticeship_level']).set_index('geography_code')
    total_total = total_total.astype(float, errors='ignore')
    stats = total_total.sum()
    print(stats)
    all_subjects.to_csv(os.path.join(OUTDIR, 'all_subjects_level_geography_code.csv'))
    all_apprenticeship_level.to_csv(os.path.join(OUTDIR, 'all_apprenticeship_level_subject_geography_code.csv'))
    total_total.to_csv(os.path.join(OUTDIR, 'all_apprenticeship_all_subject_geography_code.csv'))
    
   
    stats.to_json(os.path.join(OUTDIR, 'stats.json')) 

