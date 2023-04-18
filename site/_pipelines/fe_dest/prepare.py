import os
import sys
import pandas as pd
import re
from lookups import LA_CODES
from util import slugify

def load_data(group=None):

    #read csv
    datafile = 'data/csv/fe_dest/16-18 local authority level destinations.csv'
    data = pd.read_csv(datafile)

    if (group != None):
            data = data[data.geography_code.isin(LA_CODES[group])]

    #renaming columns
    data.rename(columns=slugify, inplace=True)

    #filtering by date and colleges and schools combined, then dropping them
    data = data[data.date == '2020/21'].drop(columns='date').reset_index()
    #data = data[data.geography_name == 'Leeds']
    data = data[data.institution_group == 'State-funded mainstream schools & colleges'].drop(columns=
    ['institution_group', 'cohort_level', 'institution_type', 'index'])

    data = data[data.characteristic_group == 'Total'].drop(columns='characteristic_group') 
    data = data[data.data_type == 'Number of pupils'].drop(columns=['data_type', 'characteristic'])

    return data

if __name__ == '__main__':

    #load the correct pipeline
    group = sys.argv[1]

    #Set up output directory
    OUTDIR = 'site/{group}/supply/fe_dest/_data/'.format(group=group)
    os.makedirs(OUTDIR, exist_ok=True)

    #load the data
    data = load_data(group=group)

    #student totals by geography
    complete_studies = data[data.cohort_level_group == 'Total'].reset_index().drop(columns='index')[['geography_code', 'cohort']].set_index('geography_code')

    dest_by_geography = data[data.cohort_level_group == 'Total'][['geography_code', 'overall', 'education','appren', 'all_work', 'all_unknown']].set_index('geography_code')
    # print(dest_by_geography.education)
    qual_level_by_geography = data[data.cohort_level_group != 'Total'].iloc[:, 0:4].reset_index().drop(columns='index')
    qual_level_by_geography = pd.pivot_table(qual_level_by_geography, values='cohort', index=['geography_code'], columns=['cohort_level_group'])
    qual_level_by_geography = qual_level_by_geography.merge(complete_studies, left_index=True, right_index=True)
    qual_level_by_geography.rename(columns=slugify, inplace=True)

    #defiing some totals and calculating percentages for each destination
    total_pupils = qual_level_by_geography.cohort
    total_sustained_dest = dest_by_geography.overall

    qual_level_by_geography['pct_level2'] = 100*qual_level_by_geography.level_2/total_pupils
    qual_level_by_geography['pct_level3'] = 100*qual_level_by_geography.level_3/total_pupils
    qual_level_by_geography['pct_all_other_qualifications'] = 100*qual_level_by_geography.all_other_qualifications/total_pupils

    #percentages for work, education, apprenticeships and not captured
    qual_level_by_geography['pct_education'] = 100*dest_by_geography.education / total_sustained_dest
    qual_level_by_geography['pct_employment'] = 100*dest_by_geography.all_work / total_sustained_dest
    qual_level_by_geography['pct_apprenticeship'] = 100*dest_by_geography.appren / total_sustained_dest
    
    #round the figures
    qual_level_by_geography=qual_level_by_geography.round(1)

    #summary
    summary = qual_level_by_geography[['all_other_qualifications',
                                       'level_2',
                                       'level_3',
                                       'cohort']].sum()


    #write to file
    qual_level_by_geography.to_csv(os.path.join(OUTDIR, 'fe_dest_totals_by_geography.csv'))
    summary.to_json(os.path.join(OUTDIR, 'summary.json'), orient='index')

