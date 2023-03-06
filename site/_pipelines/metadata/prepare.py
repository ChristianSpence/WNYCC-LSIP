import glob
import json
import logging
import os
import re
import sys

import pandas as pd
import yaml

with open('site/_pipelines/metadata/datasets.yaml', 'r') as f:
    datasets = yaml.load(f.read(), Loader=yaml.loader.BaseLoader)

logging.basicConfig(
    format="%(levelname)s:%(funcName)s:%(message)s",
    level=logging.INFO
)

SOURCE_PATH = os.path.join('data/csv')
META_DIR = os.path.join('site', 'metadata', '_data', 'source')


class SourceFile(object):
    kurtosis_clip = 50

    def __init__(self, path, base='', dimensions=[], facts=[]):
        self.filename = path
        self.metafilename = os.path.splitext(
            re.sub(r"^" + base + "/{0,1}", "", path))[0] + '.json'
        self.overridden_dimensions = dimensions
        self.overridden_facts = facts

        self.data = pd.DataFrame()

    def load_data(self):
        if self.data.empty:
            logging.debug("Reading %s", self.filename)
            self.data = pd.read_csv(
                self.filename, engine='python')

    def dimension_metadata(self, l):
        self.load_data()
        dimension = self.data.index.get_level_values(l).astype('category')
        return {
            "name": dimension.name,
            "categories": dimension.categories.to_list()
        }

    def fact_metadata(self, column_name):
        self.load_data()
        data_type = pd.api.types.infer_dtype(self.data[column_name])

        try:
            value_counts = self.data[column_name].value_counts(
                normalize=True, sort=False, bins=10)
            value_counts.index = value_counts.index.to_tuples().map(
                lambda x: ' to '.join(map(lambda v: str(round(v, 2)), x)))
        except (ValueError, TypeError):
            value_counts = self.data[column_name].value_counts(
                normalize=True, sort=True).head(10)

        value_counts = pd.DataFrame(value_counts).round(6)
        value_counts.index.name = 'value'
        value_counts.columns = ['count']
        value_counts.reset_index(inplace=True)

        return {
            "name": column_name,
            "data_type": data_type,
            "value_distribution": value_counts.to_dict(orient='records')
        }

    def metadata(self):
        self.load_data()

        try:
            dimensions = [dimension for dimension in SourceFile.guess_dimensions(
                self.data, overrides=self.overridden_dimensions, facts=self.overridden_facts)]
        except Exception as e:
            logging.error(e)
            logging.error('Problem guessing dimensions for %s', self.filename)
            logging.info('Available columns %s', self.data.columns.values)
            sys.exit(1)

        logging.debug('Guessed dimensions, %s', dimensions)

        self.data.set_index(dimensions, inplace=True)

        dimension_metadata = [self.dimension_metadata(
            l) for l in range(self.data.index.nlevels)]
        fact_metadata = [self.fact_metadata(c)
                         for c in self.data.columns.to_list()]

        return {
            "path": self.filename,
            "dimensions": dimension_metadata,
            "facts": fact_metadata,
        }

    def save_metadata(self, root=''):
        filename = os.path.join(root, self.metafilename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as f:
            f.write(json.dumps(self.metadata(), indent=2))

    @classmethod
    def guess_dimensions(cls, df, overrides=[], facts=[]):
        # First pass - let's check the data type
        types = [pd.api.types.infer_dtype(series) for _, series in df.items()]
        count_non_numeric = [len(series[pd.to_numeric(
            series.map(str).str.replace(r'[%]$', '', regex=True),
            errors='coerce'
        ).isna()].unique()) for _, series in df.items()]

        # Second pass - count the number of unique values in each column
        levels = [len(series.unique()) for _, series in df.items()]

        # Third pass - check kurtisis (how much of a tail) of values per column
        kurtosis = [series.value_counts().kurtosis()
                    for _, series in df.items()]

        model = pd.DataFrame({
            'column_name': df.columns,
            'type': types,
            'count_non_numeric': count_non_numeric,
            'levels': levels,
            'value_count_kurtosis': pd.Series(kurtosis).fillna(0),
        })

        model['test_forced_dimension'] = model.column_name.isin(overrides)
        model['test_forced_fact'] = model.column_name.isin(facts)
        model['test_string_types'] = model.type == 'string'
        model['test_column_names'] = model.column_name.str.match(
            r"(average|total|number of|count of)", case=False)
        model['test_num_as_string'] = (model.type == 'string') & (
            model.count_non_numeric != model.levels) & (model.count_non_numeric/model.levels < 0.5)
        model['test_long_tail'] = model.value_count_kurtosis > SourceFile.kurtosis_clip

        model['test_categorical_integers'] = (model.type == 'integer') & (
            model.value_count_kurtosis < SourceFile.kurtosis_clip)

        logging.debug('Model contents \n%s', model)

        # Try to guess which are levels
        dimensions = model[
            (
                model.test_forced_fact == False
            ) & (
                (
                    model.test_forced_dimension == True
                ) | (
                    (model.test_categorical_integers == True) &
                    ~(model.test_column_names == True)
                ) | (
                    (model.test_string_types == True) &
                    ~(
                        (model.test_column_names == True) |
                        (model.test_num_as_string == True)
                    )
                )
            )
        ]

        if len(model.index) == len(dimensions.index):
            logging.debug("\n\n%s", dimensions)
            raise Exception(
                'No facts left in table - all columns are potential dimensions')

        return dimensions.column_name.to_list()


def get_tree(path, ext='csv'):
    spec = os.path.join(path, '**', '*.' + ext)
    return glob.glob(spec, recursive=True)


def get_dataset_info(path, key, default=None):
    if not path in datasets:
        return default
    return datasets[path].get(key, default)


def build_metadata_files(source_path):
    metadata = [SourceFile(
        f,
        base=SOURCE_PATH,
        dimensions=get_dataset_info(f, 'dimensions', []),
        facts=get_dataset_info(f, 'facts', [])
    ) for f in get_tree(source_path)]

    for m in metadata:
        m.save_metadata(root=META_DIR)


if __name__ == '__main__':
    # SourceFile('data/csv/fe/cl-geography-detailed-202122-q4.csv',
    #            base=SOURCE_PATH).metadata()
    build_metadata_files(SOURCE_PATH)
