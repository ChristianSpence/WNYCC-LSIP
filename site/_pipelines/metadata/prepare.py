import os
import re
import glob
import json
import logging
import pandas as pd
from vars import INDEX_NAMES


logging.basicConfig(
    format="%(levelname)s:%(funcName)s:%(message)s",
    level=logging.DEBUG
)

SOURCE_PATH = os.path.join('data/csv')
META_DIR = os.path.join('site', 'metadata', '_data', 'source')


class SourceFile(object):
    def __init__(self, path, base='', reader=pd.read_csv, indexes=[]):
        self.filename = path
        self.metafilename = os.path.splitext(
            re.sub(r"^" + base + "/{0,1}", "", path))[0] + '.json'
        self.indexes = indexes

        self.reader = reader

    def metadata(self):
        logging.debug("Reading %s", self.filename)
        data = self.reader(self.filename, engine='python')
        columns = data.columns.to_list()

        indexes = [c for c in columns if c in self.indexes]
        data.set_index(indexes, inplace=True)

        def get_index_metadata(l):
            index = data.index.get_level_values(l).astype('category')
            return {
                "name": index.name,
                "categories": index.categories.to_list()
            }
        index_meta = [get_index_metadata(l) for l in range(data.index.nlevels)]

        def get_column_metadata(column_name):
            data_type = str(data[column_name].dtype)
            return {
              "name": column_name,
              "data_type": data_type,
            }
        value_meta = [get_column_metadata(c) for c in data.columns.to_list()]

        return {
            "path": self.filename,
            "indexes": index_meta,
            "values": value_meta,
        }

    def save_metadata(self, root=''):
        filename = os.path.join(root, self.metafilename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as f:
            f.write(json.dumps(self.metadata(), indent=2))


def get_tree(path, ext='csv'):
    spec = os.path.join(path, '**', '*.' + ext)
    return glob.glob(spec, recursive=True)


def build_metadata_files(source_path):
    metadata = [SourceFile(f, base=SOURCE_PATH, indexes=INDEX_NAMES)
                for f in get_tree(source_path)]
    for m in metadata:
        m.save_metadata(root=META_DIR)


if __name__ == '__main__':
    build_metadata_files(SOURCE_PATH)
