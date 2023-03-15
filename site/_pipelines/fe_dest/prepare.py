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
    data = data[data.data_type == 'Number of pupils'].drop(columns=['data_type', 'student_characteristic'])

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
    complete_studies = data[data.qualification_level == 'Total'].reset_index().drop(columns='index')[['geography_code', 'number_of_pupils_completing_16_18_study']].set_index('geography_code')

    dest_by_geography = data[data.qualification_level == 'Total'][['geography_code', 'sustained_education_apprenticeship_or_employment', 'sustained_education_destination','sustained_apprenticeships', 'sustained_employment_destination', 'activity_not_captured']].set_index('geography_code')
    # print(dest_by_geography.sustained_education_destination)
    qual_level_by_geography = data[data.qualification_level != 'Total'].iloc[:, 0:4].reset_index().drop(columns='index')
    qual_level_by_geography = pd.pivot_table(qual_level_by_geography, values='number_of_pupils_completing_16_18_study', index=['geography_code'], columns=['qualification_level'])
    qual_level_by_geography = qual_level_by_geography.merge(complete_studies, left_index=True, right_index=True)
    qual_level_by_geography.rename(columns=slugify, inplace=True)

    #defiing some totals and calculating percentages for each destination
    total_pupils = qual_level_by_geography.number_of_pupils_completing_16_18_study
    total_sustained_dest = dest_by_geography.sustained_education_apprenticeship_or_employment

    qual_level_by_geography['pct_level2'] = 100*qual_level_by_geography.level_2/total_pupils
    qual_level_by_geography['pct_level3'] = 100*qual_level_by_geography.level_3/total_pupils
    qual_level_by_geography['pct_all_other_qualifications'] = 100*qual_level_by_geography.all_other_qualifications/total_pupils

    #percentages for work, education, apprenticeships and not captured
    qual_level_by_geography['pct_education'] = 100*dest_by_geography.sustained_education_destination / total_sustained_dest
    qual_level_by_geography['pct_employment'] = 100*dest_by_geography.sustained_employment_destination / total_sustained_dest
    qual_level_by_geography['pct_apprenticeship'] = 100*dest_by_geography.sustained_apprenticeships / total_sustained_dest
    
    #round the figures
    qual_level_by_geography=qual_level_by_geography.round(1)

    #write to file
    qual_level_by_geography.to_csv(os.path.join(OUTDIR, 'fe_dest_totals_by_geography.csv'))

