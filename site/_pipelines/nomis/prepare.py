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
    #print(data2.date.max())
    industry_sector = data2[data2.date == '2021'].drop(columns='date')
    industry_sector = industry_sector.astype(float, errors='ignore')
    industry_sector = industry_sector.groupby('industry_name').sum(numeric_only=True)

    #slugify and write to file
    size_time.rename(columns=slugify, inplace=True)
    industry_sector.rename(columns=slugify, inplace=True)

    #percentage change figures
    size_time_pct_change = size_time.pct_change().dropna().mul(100).round(2)
    size_time.rename(columns={'large_250+_':'large_250_'}, inplace=True)
    size_time_indexed = pd.DataFrame()
    for i in size_time.columns:
        size_time_indexed[i] = size_time[i].div(size_time[i].iloc[0])*100
    size_time_indexed = size_time_indexed.round(2)
    #@TODO recreate abovce as an index - 2011 = 100.

    size_time.rename(columns={'large_250+_':'large_250_'}, inplace=True)
    size_time_pct_change.rename(columns={'large_250+_':'large_250_'}, inplace=True)

    #retreive the last row.
    headline_stats = size_time.iloc[-1]

    #automatic pull of stats to display on page
    nomis_date = data.date.max()
    bres_date = data2.date.max()
    largest_sector = industry_sector.obs_value.max()
    largest_sector_name = industry_sector.idxmax()[0]
    stats = pd.Series(data={'nomis_date': nomis_date, 'bres_date': bres_date, 'largest_sector_value': \
                            largest_sector, 'largest_sector_name': largest_sector_name})
    

    size_time.to_csv(os.path.join(OUTDIR, 'size_over_time_whole_region.csv'))
    industry_sector.to_csv(os.path.join(OUTDIR, 'industry_sector_latest_year.csv'))
    size_time_pct_change.to_csv(os.path.join(OUTDIR, 'size_time_pct_change.csv'))
    size_time_indexed.to_csv(os.path.join(OUTDIR, 'size_time_indexed.csv'))

    headline_stats.to_json(os.path.join(OUTDIR, 'headline_stats.json'))
    stats.to_json(os.path.join(OUTDIR, 'stats.json'))
