import sys
import os
import pandas as pd
from lookups import local_authority
import soc4

POSTINGS_BY_SOC4 = 'data/csv/datacity/JobPostingsBySOC4Code.csv'
OUT_DIR = ''


def create_path(group):
    if group is None:
        raise Exception('Please provide a group')
    dir = 'site/{group}/demand/_data/'.format(group=group)
    os.makedirs(dir, exist_ok=True)
    return dir


def read_data(path, group=None, metric=None):
    data = pd.read_csv(path)
    data.rename(columns={
        'LA': 'geography_name',
        'Thing': metric or 'metric',
        'Count': 'count',
    }, inplace=True)
    data = data.merge(local_authority, on='geography_name')

    if (group != None):
        data = data[data.group == group]

    return data


if __name__ == '__main__':
    group = sys.argv[1]
    OUT_DIR = create_path(group)

    postings_by_soc_code = read_data(
        POSTINGS_BY_SOC4, group=group, metric='soc4_code')
    postings_by_soc_code = postings_by_soc_code.merge(soc4.codes, left_on='soc4_code', right_on='unit_group')
    def name_combiner(x, y):
        return ' / '.join([x, y])
    postings_by_soc_code['sub_major_full_title'] = postings_by_soc_code.major_title.combine(postings_by_soc_code.sub_major_title, func=name_combiner)
    postings_by_soc_code['minor_full_title'] = postings_by_soc_code.sub_major_full_title.combine(postings_by_soc_code.minor_title, func=name_combiner)
    postings_by_soc_code['unit_full_title'] = postings_by_soc_code.minor_full_title.combine(postings_by_soc_code.unit_title, func=name_combiner)

    by_unit = postings_by_soc_code.pivot_table(
        columns='geography_name', index='unit_title', values='count', aggfunc=sum
      ).fillna(0).groupby(level=0).sum()
    by_unit['Total'] = by_unit.sum(axis=1)
    by_unit.sort_values('Total', ascending=False).to_csv(
        os.path.join(OUT_DIR, 'postings_by_soc4_unit.csv')
      )

    by_sub_major = postings_by_soc_code.pivot_table(
        columns='geography_name', index='sub_major_full_title', values='count', aggfunc=sum
      ).fillna(0).groupby(level=0).sum().rename(index=str.title)
    by_sub_major['Total'] = by_sub_major.sum(axis=1)
    by_sub_major.sort_values('Total', ascending=False).to_csv(
        os.path.join(OUT_DIR, 'postings_by_soc4_sub_major.csv')
      )
