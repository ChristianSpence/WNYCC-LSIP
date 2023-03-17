import os
import re

import pandas as pd

SOC4_CSV = os.path.join(os.path.dirname(__file__),
                        '../../../data/csv/lookups/soc2010.csv')


def read_codes():
    codes = pd.read_csv(SOC4_CSV, dtype={
        'sub_major_group': 'Int64',
        'minor_group': 'Int64',
        'unit_group': 'Int64',
    }).rename(columns=lambda c: re.sub(r'[-\s]+', '_', c.lower()))

    # If first digit of sub_major code doesn't match major code, set to na
    codes.loc[
        codes.major_group != (codes.sub_major_group / 10).astype("Int64"),
        ['sub_major_group', 'minor_group', 'unit_group']
    ] = None
    codes.loc[
        codes.sub_major_group != (codes.minor_group / 10).astype("Int64"),
        ['minor_group', 'unit_group']
    ] = None
    codes.loc[
        codes.minor_group != (codes.unit_group / 10).astype("Int64"),
        ['unit_group']
    ] = None

    # Clean up data
    major = codes[
        codes.sub_major_group.isna() & codes.minor_group.isna() & codes.unit_group.isna()
    ][['major_group', 'group_title']].rename(columns={'group_title': 'major_title'})

    sub_major = codes[
        ~codes.sub_major_group.isna() & codes.minor_group.isna() & codes.unit_group.isna()
    ][['sub_major_group', 'group_title']].rename(columns={'group_title': 'sub_major_title'})

    minor = codes[
        ~codes.sub_major_group.isna() & ~codes.minor_group.isna() & codes.unit_group.isna()
    ][['minor_group', 'group_title']].rename(columns={'group_title': 'minor_title'})

    codes = codes[~codes.unit_group.isna()].rename(
        columns={'group_title': 'unit_title'}
    ).merge(
        major, on='major_group', how='left'
    ).merge(
        sub_major, on='sub_major_group', how='left'
    ).merge(
        minor, on='minor_group', how='left'
    )
    return codes[[
        'unit_group',
        'major_title',
        'sub_major_title',
        'minor_title',
        'unit_title',
    ]]


codes = read_codes()
