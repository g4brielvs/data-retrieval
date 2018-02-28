#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" validate.py Checks filename for valid tags """

import csv
import glob
import json
import os
import shutil

from argparse import ArgumentParser
from collections import OrderedDict


class Tag(object):
    """
    Tag constains information about:
        - position (or index) in filename
        - valid tag (or tag)
        - valid value (or value) after correction dictionary
    """
    def __init__(self, index, value):
        self.index = index
        self.tag = self._get_valid_tag(index)
        self.value = self._get_valid_value(value)

    def __str__(self):
        return self.value

    def __repr__(self):
        return "{} : {}".format(self.tag, self.value)

    @staticmethod
    def get_tags_from_file():
        with open('tags.json') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        return list(data.keys())

    @staticmethod
    def get_corrections_from_file():
        with open('tags.json') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)

        corrections = OrderedDict()
        for k, v in data.items():
            # get the last three characters as key
            corrections[k] = OrderedDict(zip(map(lambda x: x[-3:], v), v))

        return corrections

    @staticmethod
    def dump_corrections():
        data = Tag.get_corrections_from_file()

        with open('corretions.json', mode='w+', encoding='utf-8') as f:
            json.dump(data, f)

    def _get_valid_tag(self, index):
        try:
            tag = Tag.get_tags_from_file()[index]
        except IndexError:
            tag = None

        return tag

    def _get_valid_value(self, value):
        try:
            corrections = Tag.get_corrections_from_file().get(self.tag)
            # get the last three characters as key
            return corrections.get(value[-3:], '00-n')
        except TypeError:
            return '00-n'


def validate(filename):
    """
    Checks and apply corrections in order on tags in filename

    Args:
        file (str): pathname
    """
    (name, extension) = os.path.splitext(filename)

    tags_in_filename = name.strip().split('_')
    tags = list()

    for i, item in enumerate(Tag.get_tags_from_file()):
        try:
            item_in_title = tags_in_filename[i]
        except IndexError:
            item_in_title = None

        tags.append(Tag(i, item_in_title))

    return '_'.join(map(str, tags)) + extension


def track_corrections(dst, filename):
    """
    Keeps track of corrections in the filename

    Args:
        dst (str): path to destination
    """
    new_filename = validate(filename)
    row = [filename, new_filename, filename == new_filename]

    with open(os.path.join(dst, 'corrections.csv'), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def check(src, dst):
    """
    Checks source for filenames and makes a valid copy into destination

    Args:
        src (str): path to source
        dst (str): path to destination
    """
    for pathname in glob.iglob(os.path.join(src, '**/*.csv'), recursive=True):
        (dirname, filename) = os.path.split(pathname)

        try:
            valid_filename = validate(filename)
            track_corrections(dst, filename)

            new_dst = os.path.join(dst, os.path.basename(dirname))
            new_file = os.path.join(new_dst, valid_filename)
            os.makedirs(new_dst, exist_ok=True)
            shutil.copy(pathname, new_file)

        except Exception as e:
            raise e

    # Just for the UX friendliness
    print('All files were checked! \u2714')


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-s', '--source', required=False)
    parser.add_argument('-d', '--destination', required=False, default=os.path.dirname(__file__))
    args = parser.parse_args()

    check(args.source, args.destination)
