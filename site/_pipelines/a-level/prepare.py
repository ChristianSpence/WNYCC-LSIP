import os
import sys
import pandas as pd
import re
from lookups import LA_CODES


def slugify_column_name(name):
    return re.sub(r'\s+', '_', name).replace('.', '').replace('*', '_star').lower()

def load_a_level_data(group=None):
    entries_results_file = 'data/csv/a-level/Student counts and Results - A level by region and subject (end of 16-18 study).csv'
    # entries_results_file = 'data/csv/a-level/Entries and Results - A level and AS by region and subject.csv'
    data = pd.read_csv(entries_results_file, usecols=[
        'date',
        'geography_name',
        'geography_code',
        'Institution',
        'subject_area',
        'Subject',
        'Total number of students',
        'Number at grade A*.',
        'Number at grade A.',
        'Number at grade B.',
        'Number at grade C.',
        'Number at grade D.',
        'Number at grade E.',
        'Number at grade U.',
    ])

    data = data[data.Institution == 'All state-funded schools and colleges'].drop(columns=['Institution'])
    dat = data.date.max()
    data = data[data.date == dat].drop(columns=['date'])
    data = data[data.Subject.str.startswith('Total')].drop(columns=['Subject'])

    if (group != None):
        data = data[data.geography_code.isin(LA_CODES[group])]

    data.rename(columns=slugify_column_name, inplace=True)

    return data, dat


if __name__ == '__main__':
    group = sys.argv[1]

    # Set up output directory
    OUTDIR = 'site/{group}/supply/a-level/_data/'.format(group=group)
    os.makedirs(OUTDIR, exist_ok=True)


    # prepare A-level
    data, dat = load_a_level_data(group)

    # Prepare stats data structure
    stats = data.drop(columns=['geography_name', 'geography_code']).groupby('subject_area').sum().reset_index()

    # Take the All Subjects summary line as our headline summary
    summary = stats[stats.subject_area == 'All subjects'].drop(columns=['subject_area']).sum()
    summary['csv_date'] = dat
    summary.to_json(os.path.join(OUTDIR, 'summary.json'), orient='index')

    # Remove aggregated lines
    stats = stats[~stats.subject_area.str.startswith('All ')]

    # Get totals for All students
    all_students = data[data.subject_area == 'All subjects'].drop(columns=['subject_area', 'geography_name']).set_index('geography_code')
    
    # Create totals by geography
    totals_by_geography = all_students
    totals_by_geography['pct_at_grade_a_star'] = 100 * totals_by_geography.number_at_grade_a_star / totals_by_geography.total_number_of_students
    totals_by_geography['pct_at_grade_a'] = 100 * totals_by_geography.number_at_grade_a / totals_by_geography.total_number_of_students
    totals_by_geography['pct_at_grade_b'] = 100 * totals_by_geography.number_at_grade_b / totals_by_geography.total_number_of_students
    totals_by_geography['pct_at_grade_c'] = 100 * totals_by_geography.number_at_grade_c / totals_by_geography.total_number_of_students
    totals_by_geography['pct_at_grade_d'] = 100 * totals_by_geography.number_at_grade_d / totals_by_geography.total_number_of_students
    totals_by_geography['pct_at_grade_e'] = 100 * totals_by_geography.number_at_grade_e / totals_by_geography.total_number_of_students
    totals_by_geography['pct_at_grade_u'] = 100 * totals_by_geography.number_at_grade_u / totals_by_geography.total_number_of_students
    totals_by_geography = totals_by_geography.round(1)
    totals_by_geography.to_csv(os.path.join(OUTDIR, 'a_level_totals_by_geography.csv'))

    stats['pct_at_grade_a_star'] = 100 * stats.number_at_grade_a_star / stats.total_number_of_students
    stats['pct_at_grade_a'] = 100 * stats.number_at_grade_a / stats.total_number_of_students
    stats['pct_at_grade_b'] = 100 * stats.number_at_grade_b / stats.total_number_of_students
    stats['pct_at_grade_c'] = 100 * stats.number_at_grade_c / stats.total_number_of_students
    stats['pct_at_grade_d'] = 100 * stats.number_at_grade_d / stats.total_number_of_students
    stats['pct_at_grade_e'] = 100 * stats.number_at_grade_e / stats.total_number_of_students
    stats['pct_at_grade_u'] = 100 * stats.number_at_grade_u / stats.total_number_of_students

    stats = stats.round(1)

    # Write to file
    stats.sort_values(by=['total_number_of_students'], ascending=False).to_csv(os.path.join(OUTDIR, 'a_level_by_subject.csv'), index=False)
