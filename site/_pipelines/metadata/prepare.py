import os
import re
import glob
import json
import logging
import pandas as pd
from vars import FORCED_DIMENSIONS, FORCED_FACTS


logging.basicConfig(
    format="%(levelname)s:%(funcName)s:%(message)s",
    level=logging.DEBUG
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
                self.filename, engine='python', na_values=['NA'])

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
        return {
            "name": column_name,
            "data_type": data_type,
        }

    def metadata(self):
        self.load_data()

        dimensions = [dimension for dimension in SourceFile.guess_dimensions(
            self.data, overrides=self.overridden_dimensions) if dimension not in self.overridden_facts]
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
    def guess_dimensions(cls, df, overrides=[]):
        # First pass - let's check the data type
        types = [pd.api.types.infer_dtype(series) for _, series in df.items()]
        count_non_numeric = [len(series[pd.to_numeric(
            series, errors='coerce').isna()].unique()) for _, series in df.items()]

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
        model['test_likely_types'] = (model.type == 'string') | (model.type == 'integer')
        model['test_column_names'] = model.column_name.str.match(
            r"(average|total|number of|count of)", case=False)
        model['test_num_as_string'] = (model.type == 'string') & (
            model.count_non_numeric != model.levels) & (model.count_non_numeric/model.levels < 0.5)
        model['test_long_tail'] = model.value_count_kurtosis > SourceFile.kurtosis_clip

        logging.debug('Model contents \n%s', model)

        # Try to guess which are levels
        dimensions = model[
            ( model.test_forced_dimension == True ) | (
              (model.test_likely_types == True) &
              ~(
                (model.test_column_names == True) |
                (model.test_num_as_string == True) |
                (model.test_long_tail == True)
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


def build_metadata_files(source_path):
    metadata = [SourceFile(f, base=SOURCE_PATH, dimensions=FORCED_DIMENSIONS, facts=FORCED_FACTS)
                for f in get_tree(source_path)]

    for m in metadata:
        m.save_metadata(root=META_DIR)


if __name__ == '__main__':
    # SourceFile('data/csv/fe/cl-geography-detailed-202122-q4.csv',
    #            base=SOURCE_PATH).metadata()
    build_metadata_files(SOURCE_PATH)
