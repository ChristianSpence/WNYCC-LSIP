import os
import sys
import pandas as pd
import re
from lookups import LA_CODES
from util import slugify, load_data, filtering, path_name, drop_totals

if __name__ == '__main__':

    # specify filepath
    filepath = 'data/csv/fe/Education and training geography - local authority district.csv'
    group = sys.argv[1]
    # load the data
    data = load_data(filepath, group=group, fill_na=True, na_values=['low'], value=2)

    # Handle low / na values
    data.e_and_t_aims_enrolments = data.e_and_t_aims_enrolments.fillna(0).astype(float)
    data.e_and_t_aims_ach = data.e_and_t_aims_ach.fillna(0).astype(float)

    # filter
    for i in ['e_and_t_aims_enrolments', 'e_and_t_aims_ach']:
        filtered_data = filtering(
            data, facts=i, dat='2021/22', subfilts=['sex', 'notional_nvq_level'])

        path = path_name(facts=i, subfilts=['sex', 'notional_nvq_level'],
                         dat='2021/22', group=group, stage='fe')

        # write to file
        filtered_data.to_csv(path)

    for i in ['e_and_t_aims_enrolments', 'e_and_t_aims_ach']:
        filtered_data = filtering(
            data, facts=i, dat='2021/22', subfilts=['ethnicity_group', 'notional_nvq_level'])

        path = path_name(facts=i, subfilts=['ethnicity_group', 'notional_nvq_level'],
                         dat='2021/22', group=group, stage='fe')
        # filtered_data.rename(index=slugify,inplace=True)
        # write to file
        filtered_data.to_csv(path)

    for i in ['e_and_t_aims_enrolments', 'e_and_t_aims_ach']:
        filtered_data = filtering(
            data, facts=i, dat='2021/22', subfilts=['ssa_t1_desc', 'ethnicity_group'])

        path = path_name(facts=i, subfilts=['ssa_t1_desc', 'ethnicity_group'],
                         dat='2021/22', group=group, stage='fe')
        # filtered_data.rename(index=slugify,inplace=True)
        filtered_data['total'] = filtered_data.sum(axis=1)
        # write to file
        filtered_data.to_csv(path)

    # apprenticeships
    filepath2 = 'data/csv/fe/Further education and skills geography - detailed summary.csv'
    data2 = load_data(filepath2, group=group, fill_na=True, na_values=['low'], value=2)

    # Handle low / na values
    data2.participation = data2.participation.fillna(0).astype(float)
    data2.achievements = data2.achievements.fillna(0).astype(float)

    for i in ['participation', 'achievements']:
        apprenticeships = data2[data2.apprenticeships_or_further_education ==
                                'Apprenticeships']
        apprenticeships = filtering(
            apprenticeships, facts=i, dat='2021/22', subfilts=['level_or_type', 'age_group'])

        path = path_name(facts=i, subfilts=['level_or_type', 'age_group'],
                         dat='2021/22', group=group, stage='fe')
        # apprenticeships.rename(index=slugify,inplace=True)
        # write to file
        apprenticeships.to_csv(path)
        