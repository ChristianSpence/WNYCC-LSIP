import os

import pandas as pd

GEO_CSV = os.path.abspath(os.path.join(os.path.dirname(
    __file__), '../../data/csv/lookups/geography.csv'))

geography = pd.read_csv(GEO_CSV)


LA_CODES = {
    'wycc': ['E08000032',
             'E08000033',
             'E08000034',
             'E08000035',
             'E08000036',
             ],
    'nycc': ['E06000014',
             'E07000163',
             'E07000164',
             'E07000165',
             'E07000166',
             'E07000167',
             'E07000168',
             'E07000169',
             ]
             }

local_authority = pd.DataFrame({
    'geography_code': pd.Series(LA_CODES).explode()
}).reset_index().merge(geography, on='geography_code')
local_authority.rename(columns={'index': 'group'}, inplace=True)
