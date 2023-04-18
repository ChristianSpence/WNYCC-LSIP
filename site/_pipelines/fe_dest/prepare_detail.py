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

    data = load_data(filepath, group='wycc')
    date = data.date.max()
    dat = pd.Series(data={'date': date})
    GD_data = data[data.date == date].drop(columns='date')
    GD_data = GD_data[GD_data.institution_group == 'State-funded mainstream schools & colleges'].drop(columns= ['institution_group', 'cohort_level', 'institution_type'])
    GD_data = GD_data[GD_data.data_type != 'Percentage'].drop(columns=['data_type'])
    GD_data = drop_totals(GD_data)
    GD = GD_data.groupby('characteristic').sum(numeric_only=True)

    data = data[data.date == date].drop(columns='date')
    SEN_data = data.drop(columns=['institution_type', 'cohort_level'])
    SEN_data = SEN_data[SEN_data.data_type != 'Percentage'].drop(columns=['data_type'])
    SEN_data = drop_totals(SEN_data)
    LLDD = SEN_data[SEN_data.characteristic_group == 'LLDD Provision'].groupby('characteristic').sum(numeric_only=True)
    SEN = SEN_data[SEN_data.characteristic_group == 'SEN Provision'].groupby('characteristic').sum(numeric_only=True)

    frames = [LLDD, SEN, GD]
    result = pd.concat(frames)

    OUTDIR = 'site/{group}/supply/fe_dest/_data/2020_21/'.format(group=group)
    os.makedirs(OUTDIR, exist_ok=True)
    result.to_csv(os.path.join(OUTDIR, 'fe_dest_detail.csv'))
    dat.to_json(os.path.join(OUTDIR, 'date.json'), orient='index')
    # for i in ['fe_level_3']:
    #     filtered_SEN_data = filtering(
    #         SEN_data, facts=i, dat='2020/21', subfilts=['characteristic_group', 'student_characteristic'])
    #         filtered_SEN_data = filtered_SEN_data.loc[["LLDD Provision", "SEN Provision"]].drop(columns=['Disadvantaged', 'Female', 'Male', 'Not Disadvantaged'])
    #@TODO find way to merge with above to avoid wriitng to separate file.
    


    #@TODO add code below to get visualisations for people going on to apprenticeships at levels 2, 3, 4. 
    # for i in ['higher_and_degree_apprenticeships_level_4_and_above', 'advanced_apprenticeships_level_3', 'intermediate_apprenticeships_level_2']:
    #     filtered_data = filtering(
    #         data, facts=i, dat='2020/21', subfilts=['characteristic_group', 'student_characteristic'])

    #     path = path_name(facts=i, subfilts=['characteristic_group', 'student_characteristic'],
    #                      dat='2020/21', group=group, stage='fe_dest')
        
    #     # write to file
    #     filtered_data.to_csv(path)
