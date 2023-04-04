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
    data = data.replace(['low'], 0)
    all_subjects = data[data.ssa_t1_desc == 'Total'].drop(columns='ssa_t1_desc')
    all_subjects = all_subjects[all_subjects.apprenticeship_level != 'Total'].reset_index()
    all_subjects_starts = all_subjects.pivot(index='geography_code', columns='apprenticeship_level', values='starts')
    all_subjects_ach = all_subjects.pivot(index='geography_code', columns='apprenticeship_level', values='achievements')
    
    all_apprenticeship_level = data[data.apprenticeship_level == 'Total'].drop(columns='apprenticeship_level')
    all_apprenticeship_level = all_apprenticeship_level[all_apprenticeship_level.ssa_t1_desc != 'Total'].reset_index()
    all_apprenticeship_level_starts = all_apprenticeship_level.pivot(index='geography_code', columns='ssa_t1_desc', values='starts')
    all_apprenticeship_level_ach = all_apprenticeship_level.pivot(index='geography_code', columns='ssa_t1_desc', values='achievements')

    total_total = data[(data.ssa_t1_desc == 'Total') & (data.apprenticeship_level == 'Total')].set_index('geography_code')
    total_total = total_total.astype(float, errors='ignore').drop(columns=['ssa_t1_desc', 'apprenticeship_level'])
    stats = total_total.sum(numeric_only=True)
    
    #WRITE TO FILES
    all_subjects_starts.to_csv(os.path.join(OUTDIR, 'all_subjects_level_geography_code_starts.csv'))
    all_subjects_ach.to_csv(os.path.join(OUTDIR, 'all_subjects_level_geography_code_ach.csv'))

    all_apprenticeship_level_starts.to_csv(os.path.join(OUTDIR, 'all_apprenticeship_level_subject_geography_code_starts.csv'))
    all_apprenticeship_level_ach.to_csv(os.path.join(OUTDIR, 'all_apprenticeship_level_subject_geography_code_ach.csv'))

    total_total.to_csv(os.path.join(OUTDIR, 'all_apprenticeship_all_subject_geography_code.csv'))
    
   
    stats.to_json(os.path.join(OUTDIR, 'stats.json')) 

