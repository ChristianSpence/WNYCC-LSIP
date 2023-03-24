import os
import sys
import pandas as pd
import re
from lookups import LA_CODES
from util import slugify, load_data, filtering, path_name, drop_totals

if __name__ == '__main__':

    # specify filepath
    filepath = 'data/csv/fe_dest/16-18 local authority level destinations.csv'
    group = sys.argv[1]

    data = load_data(filepath, group=group, fill_na=True, na_values=['NA'], value=0)
    data = data[data.institution_group == 'State-funded mainstream schools & colleges'].drop(columns=
    ['institution_group', 'cohort_level', 'institution_type'])
    data = data[data.data_type != 'Percentage'].drop(columns=['data_type'])

    data = drop_totals(data)
    # , 'fe_level_2', 'fe_entry_level_and_no_identified_level', 'other_education_destinations'
    for i in ['fe_level_3', 'fe_level_2', 'fe_entry_level_and_no_identified_level', 'other_education_destinations']:
        filtered_data = filtering(
            data, facts=i, dat='2020/21', subfilts=['characteristic_group', 'student_characteristic'])

        path = path_name(facts=i, subfilts=['characteristic_group', 'student_characteristic'],
                         dat='2020/21', group=group, stage='fe_dest')
        #filtered_data.fillna(0)
        # write to file
        filtered_data.to_csv(path)
