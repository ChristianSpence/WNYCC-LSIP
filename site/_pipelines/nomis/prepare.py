import os
import sys
import pandas as pd
import re
from lookups import LA_CODES
from util import slugify, load_data, drop_totals

if __name__ == '__main__':
    filepath = 'data/csv/nomis/ukbc-lu-emp.csv'
    group = sys.argv[1]
    OUTDIR = 'site/{group}/demand/nomis/_data/'.format(group=group)
    os.makedirs(OUTDIR, exist_ok=True)

    #load and filter UKBC data
    data = load_data(filepath, group=group, fill_na=False)
    size_time = data.drop(columns=['industry_code', 'industry_name'])
    size_time = data.groupby(['date', 'employment_sizeband_name']).sum(numeric_only=True).reset_index()
    size_time = size_time.pivot(index='date', columns='employment_sizeband_name', values='obs_value')
    
    #load and filter BRES data
    filepath2 = 'data/csv/nomis/bres.csv'
    data2 = load_data(filepath2, group=group, fill_na=False)
    data2 = data2.astype({'date': 'str'})
    industry_sector = data2[data2.date == '2021'].drop(columns='date')
    #print(industry_sector)
    industry_sector = industry_sector.astype(float, errors='ignore')
    industry_sector = industry_sector.groupby('industry_name').sum(numeric_only=True)

    #write to file
    size_time.to_csv(os.path.join(OUTDIR, 'size_over_time_whole_region.csv'))
    industry_sector.to_csv(os.path.join(OUTDIR, 'industry_sector_latest_year.csv'))