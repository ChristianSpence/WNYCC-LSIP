import os
import sys
import pandas as pd
import re
from lookups import LA_CODES

def slugify(s):
    #TODO try replace '\W+'
    return re.sub(r'[\*\-\(\)\s\,\"\(/)]+', '_', s.lower())

def load_data(filepath, group=None, fill_na=True, value=2):
    '''
    Read the data in filepath. 
    If fill_na=True, replace NaN values with value.
    
    Inputs
    ------
    filepath: str - contains the csv file
    group: str - county
    fill_na: boolean
    value: float64
    
    Returns
    ------
    data frame with slugified column names
    '''

    #read csv
    if fill_na == True:
        data = pd.read_csv(filepath, na_values=['low'])
        data.update(data.iloc[:, list(data.dtypes == 'float64')].fillna(value))
        
    else:
        data = pd.read_csv(filepath)
    
    #filtering by CoC
    if (group != None):
            data = data[data.geography_code.isin(LA_CODES[group])].drop(columns='geography_name')
    
    #renaming columns
    data.rename(columns=slugify, inplace=True)
    
    return data

def filtering(data, facts=None, dat=None, subfilts=None, drop_columns=None):
    '''
    Filters the data.
    
    Inputs
    ------
    data: pandas dataframe
    facts: str - the measurable you want out #check length
    dat: str - date in form yyyy/yy e.g. 2020/21
    subfilts: lst of str - two variables to filter by. first should be the one you want to index by.
    
    Returns
    -------
    filtered data frame
    '''
    if dat != None:
        data = data[data.date == dat].drop(columns='date')
    
    if subfilts != None:
        data = drop_totals(data, drop_columns)
        data = data.groupby(subfilts).sum(numeric_only=True).reset_index().pivot(columns=subfilts[1], index=subfilts[0], values=facts)
        
    
    return data

def path_name(facts, subfilts, dat, group, stage, OUTDIR=None):
    '''Takes data and writes it to a file with name 
        fact_subfilter1_subfilter2.csv
        
    Inputs
    ------
    facts: the measurable quantity
    subfilts: two filters, become names of the output file
    dat: date in form yyyy/yy e.g. 2020/21
    group: wycc/nycc
    stage: catgegory e.g.  a_level, fe, fe_dest, he, ks4
    OUTDIR: output directory
    
    Returns
    -------
    csv file containing data
    '''
    dat = slugify(dat)
    
    if OUTDIR == None:
        #OUTDIR = 'site/{group}/supply/{stage}/_data/{date}'.format(group=group, stage=stage, date=dat)
        OUTDIR = 'site/{group}/supply/{stage}/_data/{dat}/'.format(group=group, stage=stage, dat=dat)
    os.makedirs(OUTDIR, exist_ok=True)
    ##construct filenames based on cols/index
    
    return os.path.join(OUTDIR, '{x}_{y}_{z}.csv'.format(x=facts, y=subfilts[0], z=subfilts[1]))

def drop_totals(data, drop_columns=None):
    for col in drop_columns or data.columns:
        try:
            data = data[~data[col].str.contains('Total')]
        except:
            pass
    return data