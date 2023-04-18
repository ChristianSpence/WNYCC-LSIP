import os
import sys

import pandas as pd

from util import slugify

LA_CODES = {
    'wycc': ['E08000032',
             'E08000033',
             'E08000034',
             'E08000035',
             'E08000036'],
    'nycc': ['E06000014',
             'E07000163',
             'E07000164',
             'E07000165',
             'E07000166',
             'E07000167',
             'E07000168',
             'E07000169',
             ]}


def read_data(region=None):
    data = pd.read_csv('data/csv/ks4/Key stage 4 performance.csv')
    if region:
        data = data[data.geography_code.isin(LA_CODES[region])]
    return data


if __name__ == '__main__':
    region = sys.argv[1]
    OUTDIR = os.path.join('site', region, 'supply', 'ks4', '_data')
    os.makedirs(OUTDIR, exist_ok=True)

    data = read_data(region)
    dat = data.date.max()
    data = data[data.date == dat]

    # Select key stats
    stats = data[[
        'geography_code',
        'Average Attainment 8 score of all pupils',
        'Total number of schools',
        'Total number of pupils at the end of key stage 4',
        'Total number of pupils entering English and Mathematics GCSEs',
        'Total number of pupils entering the English Baccalaureate',
        'Average EBacc APS score per pupil',
        'Total number of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)',
        'Total number of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)',
        'Total number of pupils achieving grades 4 or above in English and Mathematics GCSEs',
        'Total number of pupils achieving grades 5 or above in English and Mathematics GCSEs',
        'Percentage of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)',
        'Percentage of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)',
        'Percentage of pupils achieving grades 4 or above in English and Mathematics GCSEs',
        'Percentage of pupils achieving grades 5 or above in English and Mathematics GCSEs',
    ]]
    stats.set_index(['geography_code'], inplace=True)

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
    ]].sum()
    summary['csv_date'] = dat
    summary.to_json(os.path.join(OUTDIR, 'summary.json'), orient='index')

    totals_by_area = stats[[
      "total_number_of_pupils_achieving_the_english_baccalaureate_grades_5_or_above",
      "total_number_of_pupils_achieving_the_english_baccalaureate_grades_4_or_above",
      "total_number_of_pupils_achieving_grades_5_or_above_in_english_and_mathematics_gcse",
      "total_number_of_pupils_achieving_grades_4_or_above_in_english_and_mathematics_gcse",
    ]].transpose()
    totals_by_area.index.names=["measure"]
    
    totals_by_area.to_csv(os.path.join(OUTDIR, 'totals_by_geography.csv'))

    percentage_by_area = stats[[
      "percentage_of_pupils_achieving_the_english_baccalaureate_grades_5_or_above",
      "percentage_of_pupils_achieving_the_english_baccalaureate_grades_4_or_above",
      "percentage_of_pupils_achieving_grades_5_or_above_in_english_and_mathematics_gcse",
      "percentage_of_pupils_achieving_grades_4_or_above_in_english_and_mathematics_gcse",
    ]].transpose().astype('float')
    percentage_by_area.index.names=["measure"]
    
    percentage_by_area.to_csv(os.path.join(OUTDIR, 'percentage_by_geography.csv'))
