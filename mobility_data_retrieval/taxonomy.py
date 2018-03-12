#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" taxonomy.py Creates and handles the taxonomy """

import json

import pandas as pd

from argparse import ArgumentParser
from collections import OrderedDict

class Taxonomy(object):
    """
    Taxonomy constains information about the tags
    """
    def __init__(self, data=dict()):
        if isinstance(data, dict):
            self.taxonomy = data
        elif isinstance(data, str):
            self.taxonomy = self._read_taxonomy(data)

    def __str__(self):
        return self.taxonomy

    def filter(self, names={}):
        """
        Filter taxonomy using tag names

        Args:
            data (dict): taxonomy
            names (set): set with names as filter criteria
        """
        return dict(filter(lambda i:i[1].get('nameSeq') in names, self.taxonomy.items()))

    def get_tags(self):
        """
        Get list of tags from taxonomy
        """
        return list(self.taxonomy.keys())

    def get_text_from_tag(self, tag=None, key='txID'):
        """
        Get text description from taxonomy

        Args:
            data (dict): taxonomy
            tag (str): tag id
            key: (str): key of description
        """
        return self.taxonomy.get(tag).get(key)

    def dump_taxonomy_to_file(self, dst='taxonomy.json', encoding='utf-8'):
        """
        Dump taxonomy into JSON file

        Args:
            src (pathname): path to JSON file
        """
        try:
            with open(dst, mode='w+', encoding=encoding) as f:
                json.dump(self.taxonomy, f)
                print('Taxonomy successfully exported! \u2714')
        except Exception as e:
            raise e

    def _read_taxonomy(self, pathname):
        """
        Read taxonomy from JSON file

        Args:
            src (pathname): path to JSON file
        """
        with open(pathname) as f:
            return json.load(f, object_pairs_hook=OrderedDict)

def get_header(src, encoding='cp1252'):
    """
    Get header from the data structure file

    Args:
        src (str): path to the data structure file
    """
    df = pd.read_csv(src, sep=',', encoding=encoding)
    return list(df.columns.values)

def get_names(src, encoding='cp1252', column_slice=1):
    """
    Get tag names from file

    Args:
        src (str): path to the data structure file
    """
    return list(pd.read_csv(src, encoding=encoding, header=None).iloc[:, column_slice])

def get_taxonomy_from_file(src, encoding='cp1252', key='txID'):
    """
    Creates a taxonomy pivoting with key

    Args:
        src (str): path to the data structure file
    """
    data = OrderedDict()
    df = pd.read_csv(src, sep=',', converters={key: lambda x: str(x)}, encoding=encoding)

    HEADER = get_header(src, encoding)

    for _, row in df.iterrows():
        data[row[key]] = OrderedDict(((i, row[i]) for i in HEADER))

    return data

def fix_taxonomy_from_file(data=dict(), names=list()):
    """
    Fixes a dictionary if default keys

    Args:
        src (str): path to the data structure file
    """

    for i, item in enumerate(names, 1):
        key = '{:02}00-nr'.format(i)
        if key not in data:
            data[key] = {'nameSeq' : i, 'txID' : key}
        key = '{:02}99-na'.format(i)
        if key not in data:
            data[key] = {'nameSeq' : i, 'txID' : key}
    return data

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-s', '--source', required=True)
    parser.add_argument('-n', '--names', required=False)
    args = parser.parse_args()

    tax = get_taxonomy_from_file(args.source)
    tax = fix_taxonomy_from_file(tax, get_names(args.names))

    t = Taxonomy(tax)
    t.dump_taxonomy_to_file()
