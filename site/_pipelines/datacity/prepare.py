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


def name_combiner(x, y):
    return ' / '.join([x, y])


if __name__ == '__main__':
    group = sys.argv[1]
    OUT_DIR = create_path(group)

    postings_by_soc_code = read_data(
        POSTINGS_BY_SOC4, group=group, metric='soc4_code')
    postings_by_soc_code = postings_by_soc_code.merge(
        soc4.codes, left_on='soc4_code', right_on='unit_group')

    postings_by_soc_code['sub_major_full_title'] = postings_by_soc_code.major_title.combine(
        postings_by_soc_code.sub_major_title, func=name_combiner)
    postings_by_soc_code['minor_full_title'] = postings_by_soc_code.sub_major_full_title.combine(
        postings_by_soc_code.minor_title, func=name_combiner)
    postings_by_soc_code['unit_full_title'] = postings_by_soc_code.minor_full_title.combine(
        postings_by_soc_code.unit_title, func=name_combiner)

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

    by_sub_major.sum().to_json(os.path.join(OUT_DIR, 'postings_summary.json'), indent=2)

    skill_postings = read_data(
        'data/csv/datacity/JobPostingsBySpecializedSkill.csv',
        group=group,
        metric='skill'
    )
    skill_duration = read_data(
        'data/csv/datacity/AveragePostingDurationBySpecializedSkill.csv',
        group=group,
        metric='skill'
    ).rename(columns={
        'count': 'duration',
    })

    skill_postings = skill_postings.merge(skill_duration)

    skill_postings.set_index(['geography_code', 'geography_code', 'skill']).drop(
        columns=['group']).to_csv(os.path.join(OUT_DIR, 'skills_demand_duration.csv'))

    # Calcualte the postings hierarchy
    postings_hierarchy = postings_by_soc_code

    # Clip the smaller postings (less than 0.5%)
    clip = postings_by_soc_code['count'].sum() * 0.005
    postings_hierarchy.loc[postings_hierarchy['count']
                           < clip, ['major_title', 'sub_major_title', 'minor_title', 'unit_title']] = 'All other postings'

    postings_hierarchy.groupby([
        'major_title', 'sub_major_title', 'minor_title', 'unit_title'
    ])['count'].sum().to_csv(os.path.join(OUT_DIR, 'postings.csv'))
