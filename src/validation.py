#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" validation.py Validates filenames with taxonomy """

import csv
import glob
import os

from argparse import ArgumentParser

from taxonomy import Taxonomy

def check(src, taxonomy=Taxonomy()):
    """
    Validates filename with taxonomy

    Args:
        src (str): path to source
    """
    (dirname, filename) = os.path.split(pathname)
    (name, extension) = os.path.splitext(filename)

    tags = name.strip().split('_')

    for i, tag in enumerate(tags, 1):
        possible_tags = taxonomy.filter(names={i}).keys()
        if tag not in possible_tags:
            return False
    return True

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-s', '--source', required=True)
    parser.add_argument('-t', '--taxonomy', required=False, default='taxonomy.json')
    args = parser.parse_args()

    taxonomy = Taxonomy(args.taxonomy)

    for pathname in glob.iglob(os.path.join(args.source, '**/*.csv'), recursive=True):

        with open('validation.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([pathname, check(pathname, taxonomy)])
