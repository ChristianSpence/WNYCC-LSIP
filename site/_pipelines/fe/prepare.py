import os
import sys
import pandas as pd
import re
from lookups import LA_CODES
from util import slugify

def load_data(filepath, group=None):

    #read csv
    data = pd.read_csv(filepath)

    #filtering by CoC
    if (group != None):
            data = data[data.geography_code.isin(LA_CODES[group])].drop(columns='geography_name')

    #renaming columns
    data.rename(columns=slugify, inplace=True)

    return data

if __name__ == '__main__':
    
    #load the correct pipeline
    group = sys.argv[1]

    #Set up output directory
    OUTDIR = 'site/{group}/supply/fe/_data/'.format(group=group)
    os.makedirs(OUTDIR, exist_ok=True)

    #load the data
    data = load_data('data/csv/fe/Basic skills - regional breakdown.csv', group)

    #temp data filter
    #data = data[data.geography_code == 'E08000032']
    mycols = ['Basic Skills (Excluding digital skills)', 'Basic Skills (Including digital skills)','ESOL', 'Maths', 'English', 'Essential Digital Skills']
    

    basic_skills = data[data.age_youth_adult == 'Total'].drop(columns=['age_youth_adult', 'date']).set_index('subject_level', drop=False)
    basic_skills = basic_skills.loc[mycols].set_index('geography_code')
    
    if group == 'nycc':
        basic_skills = basic_skills.replace(to_replace=r'^lo.$', value=0, regex=True)
    #print(basic_skills)
    

    #making stuff numeric
    for k in ['achievements', 'participation']:
         basic_skills[k] = pd.to_numeric(basic_skills[k])

    #slugify colnames
    basic_skills.rename(columns=slugify, inplace=True)

    #achievement to participation ratio
    stats = basic_skills.groupby('geography_code').sum(numeric_only=True)
    stats['ap_ratio'] = stats.achievements / stats.participation
    

    stats['eng_participation'] = basic_skills[basic_skills.subject_level == 'English'].participation
    stats['maths_participation'] = basic_skills[basic_skills.subject_level == 'Maths'].participation
    stats['esol_participation'] = basic_skills[basic_skills.subject_level == 'ESOL'].participation
    stats['eds_participation'] = basic_skills[basic_skills.subject_level == 'Essential Digital Skills'].participation

    stats['eng_achievements'] = basic_skills[basic_skills.subject_level == 'English'].achievements
    stats['maths_achievements'] = basic_skills[basic_skills.subject_level == 'Maths'].achievements
    stats['esol_achievements'] = basic_skills[basic_skills.subject_level == 'ESOL'].achievements
    stats['eds_achievements'] = basic_skills[basic_skills.subject_level == 'Essential Digital Skills'].achievements

    stats=stats.round(2)

    fe_and_skills = load_data('data/csv/fe/Further education and skills geography - detailed summary.csv', group)
    fe_and_skills = fe_and_skills[fe_and_skills.age_group == 'Total'].drop(columns=['age_group'])
    fe_and_skills = fe_and_skills[fe_and_skills.date == '2021/22']
    fe_and_skills  = fe_and_skills[fe_and_skills.level_or_type.str.endswith('Total')].drop(columns=['new_la_code', 'date', 'la_name', 'level_or_type']).set_index('geography_code')

    e_and_t = load_data('data/csv/fe/Education and training geography - local authority district.csv', group)
    e_and_t = e_and_t.replace(to_replace=r'^lo.$', value=0, regex=True)
    e_and_t = e_and_t[(e_and_t.date == '2021/22') & (e_and_t.sex == 'Total') & (e_and_t.ethnicity_group == 'Total')].drop(columns=[
                                                                                'date', 'sex', 'ethnicity_group', 'notional_nvq_level']).set_index('ssa_t1_desc')
    
    for k in ['e_and_t_aims_enrolments', 'e_and_t_aims_ach']:
         e_and_t[k] = pd.to_numeric(e_and_t[k])
    e_and_t.drop(['Total'],inplace=True)
    e_and_t = e_and_t.groupby('ssa_t1_desc').sum(numeric_only=True)

    summary = stats.drop(columns='ap_ratio').sum()
    #print(e_and_t)

    #write to file
    basic_skills.to_csv(os.path.join(OUTDIR, 'basic_skills.csv'))
    fe_and_skills.to_csv(os.path.join(OUTDIR, 'fe_type.csv'))
    e_and_t.sort_values(by=['e_and_t_aims_enrolments'], ascending=False).to_csv(os.path.join(OUTDIR, 'e_and_t_by_ssa_t1_desc.csv'))
    stats.to_csv(os.path.join(OUTDIR, 'stats.csv'))
    summary.to_json(os.path.join(OUTDIR, 'summary.json'))

      
