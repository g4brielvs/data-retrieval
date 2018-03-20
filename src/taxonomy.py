#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" taxonomy.py Creates and handles the taxonomy """

import os
import json

import pandas as pd

from argparse import ArgumentParser
from collections import OrderedDict

class Taxonomy(object):
    """
    Taxonomy constains information about the tags
    """
    def __init__(self, data=dict(), prefix='not set', pivot='not set'):
        if isinstance(data, dict):
            self.taxonomy = data
            self.prefix = prefix
            self.pivot = pivot
        elif isinstance(data, str):
            self.taxonomy = self._read_taxonomy(data)
            self.prefix = prefix
            self.pivot = pivot

    def __repr__(self):
        return 'Taxonomy (id={}) constains {} tags with prefix {}.'.format(id(self), len(self.taxonomy), self.prefix)

    def filter(self, criteria='index', selection={}):
        """
        Filter the taxonomy using criteria and selection

        Args:
            criteria (str): criteria for filter
            selection (set): selection for filter
        """
        return dict(filter(lambda i:i[1].get(criteria) in selection, self.taxonomy.items()))

    def get_tags(self):
        """
        Get list of tags from taxonomy
        """
        return list(self.taxonomy.keys())

    def get_text_from_tag(self, tag=None, name='txID'):
        """
        Get text description from taxonomy

        Args:
            tag (str): tag id
            name: (str): key of description
        """
        try:
            return self.taxonomy.get(tag).get(name)
        except AttributeError as e:
            return 'Not found in the taxonomy.'

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

def get_taxonomy_from_file(src, encoding='utf-8', tags=[], prefix='', names=[], pivot='', position=True):
    """
    Creates a dictionary from tags and names into a taxonomy

    Args:
        src (str): path to the data structure directory
        tags (list): list of tags
        names (list): list of names
        prefix (str): prefix for searching data structure
        pivot (str): select key of the dictionary
        position (bool): select whether prefix position of tag in the dictionary
    """
    taxonomy = dict()

    for i, tag in enumerate(tags, 1):
        pathname = os.path.join(src, '{}{}.csv'.format(prefix, tag))
        df = pd.read_csv(pathname, sep=',', names=names, converters={pivot: lambda x: str(x)}, encoding=encoding)

        for _, row in df.iterrows():

            if position:
                key = '{}-{}'.format(i, row[pivot])
            else:
                key = '{}'.format(row[pivot])

            data = OrderedDict({'index' : i})
            data.update(OrderedDict(((v, row[index]) for index, v in enumerate(names))))
            taxonomy[key] = data

    return taxonomy

def fix_taxonomy_from_file(data=dict(), names=list()):
    """
    Fixes a dictionary with default keys

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

def get_column_from_file(pathname, encoding='utf-8', index=0):
    """
    Get column as a list from file

    Args:
        src (str): path to the data structure file
    """
    return list(pd.read_csv(pathname, encoding=encoding, header=None).iloc[:, index])

def get_tag_from_file(pathname, index=0):
    """
    Get tag from nth position in filename

    Args:
        src (str): path to the data structure file
    """
    (dirname, filename) = os.path.split(pathname)
    (name, extension) = os.path.splitext(filename)

    try:
        return name.strip().split('_')[index]
    except Exception as e:
        raise e

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-s', '--source', required=True)
    parser.add_argument('-t', '--tags', required=False)
    parser.add_argument('-n', '--names', required=False)
    args = parser.parse_args()

    taxonomy = get_taxonomy_from_file(src=args.source, tags=args.tags, names=args.names)
    taxonomy = fix_taxonomy_from_file(taxonomy)

    Taxonomy(taxonomy).dump_taxonomy_to_file()
