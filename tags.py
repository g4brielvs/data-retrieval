#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" tags.py Creates tags for checking filenames """

import json
import os

from argparse import ArgumentParser


def create(src, first_row, last_row):
    """
    Creates a dictionary of tags from the provided information

    Args:
        src (str): path of source
        first_row (int): first row to read
        last_row (int): last row to read
    """

    with open(src, mode='r', encoding='utf-16') as f:
        content = f.readlines()[first_row:last_row]

    # Creates a dict using the second column as key and the rest as value
    data = dict([(line.split()[1], line.split()[2:]) for line in content])

    return data


def dump(dst, data):
    """
    Dumps a dictionary of tags into a JSON

    Args:
        dst (str): path of destination
        tags (dict): dictionary of tags
    """
    try:
        with open(os.path.join(dst, 'tags.json'), mode='w+', encoding='utf-8') as f:
            json.dump(data, f)
            print('Tags successfully exported! \u2714')
    except Exception as e:
        raise e


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-s', '--src', required=True)
    parser.add_argument('-d', '--dst', default=os.path.dirname(__file__))
    parser.add_argument('--first_row', help='First row to read', default=5)
    parser.add_argument('--last_row', help='Last row to read', default=21)
    args = parser.parse_args()

    tags = create(args.src, int(args.first_row), int(args.last_row))
    dump(args.dst, tags)
