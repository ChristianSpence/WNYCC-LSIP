import os
import sys

import pandas as pd

from util import slugify

LA_CODES = {
    'wycc': ['E08000032', 'E08000033', 'E08000034', 'E08000035', 'E08000036'],
}


def read_data(region=None):
    data = pd.read_csv('data/csv/ks4/ks4.csv')
    if region:
        data = data[data.geography_code.isin(LA_CODES[region])]
    return data


if __name__ == '__main__':
    region = sys.argv[1]
    OUTDIR = os.path.join('site', region, 'supply', 'ks4', '_data')
    os.makedirs(OUTDIR)

    data = read_data(region)

    # Select key stats
    stats = data[[
        'date',
        'geography_code',
        'Average Attainment 8 score of all pupils',
        'Total number of schools',
        'Total number of pupils at the end of key stage 4',
        'Total number of pupils entering English and Mathematics GCSEs',
        'Total number of pupils entering the English Baccalaureate',
        'Total number of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)',
        'Total number of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)',
        'Total number of pupils achieving grades 4 or above in English and Mathematics GCSEs',
        'Total number of pupils achieving grades 5 or above in English and Mathematics GCSEs',
        'Percentage of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)',
        'Percentage of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)',
        'Percentage of pupils achieving grades 4 or above in English and Mathematics GCSEs',
        'Percentage of pupils achieving grades 5 or above in English and Mathematics GCSEs',
    ]]
    stats.date = stats.date.str.replace('/', '-')
    stats.set_index(['date', 'geography_code'], inplace=True)

    # Rename columns
    stats = stats.rename(columns={
        'Total number of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)':
          'Total number of pupils achieving the English Baccalaureate grades 4 or above',
        'Total number of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)':
          'Total number of pupils achieving the English Baccalaureate grades 5 or above',
        'Total number of pupils achieving grades 4 or above in English and Mathematics GCSEs':
          'Total number of pupils achieving grades 4 or above in English and Mathematics GCSE',
        'Total number of pupils achieving grades 5 or above in English and Mathematics GCSEs':
          'Total number of pupils achieving grades 5 or above in English and Mathematics GCSE',
        'Percentage of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)':
          'Percentage of pupils achieving the English Baccalaureate grades 4 or above',
        'Percentage of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)':
          'Percentage of pupils achieving the English Baccalaureate grades 5 or above',
        'Percentage of pupils achieving grades 4 or above in English and Mathematics GCSEs':
          'Percentage of pupils achieving grades 4 or above in English and Mathematics GCSE',
        'Percentage of pupils achieving grades 5 or above in English and Mathematics GCSEs':
          'Percentage of pupils achieving grades 5 or above in English and Mathematics GCSE',
    })
    stats = stats.rename(columns=slugify)

    stats['pupil_to_school_ratio'] = (stats.total_number_of_pupils_at_the_end_of_key_stage_4 / \
        stats.total_number_of_schools).round(1)

    stats.to_csv(os.path.join(OUTDIR, 'stats.csv'))

    summary = stats[[
        'total_number_of_schools',
        'total_number_of_pupils_at_the_end_of_key_stage_4',
        'total_number_of_pupils_entering_english_and_mathematics_gcses',
        'total_number_of_pupils_entering_the_english_baccalaureate',
    ]].groupby('date').sum()

    summary.to_json(os.path.join(OUTDIR, 'summary.json'), orient='index')
