#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" create_tags.py Creates tags for checking filenames """

import json
import os
import sys

def create(src, first_row, last_row):
    """
    Creates a dictionary of tags from the provided information

    Args:
        src (str): path of source
        first_row (int): first row to read
        last_row (int): last row to read
    """

    with open(src, mode="rt", encoding="utf-16") as f:
        content = f.readlines()[first_row:last_row]

    data = [dict([(line.split()[1], line.split()[2:])]) for line in content]

    return data

def dump(dst, data):
    """
    Dumps a dictionary of tags into a JSON

    Args:
        dst (str): path of destination
        tags (dict): dictionary of tags
    """

    with open(os.path.join(dst,'tags.json'), mode='w+', encoding='utf-8') as f:
        json.dump(data, f)

if __name__ == '__main__':

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-s', '--source', help='Path to source file', required=True)
    parser.add_argument('-d', '--destination', help='Path to destination file', default=os.path.dirname(__file__))
    parser.add_argument('--first_row', help='First row to read', default=5)
    parser.add_argument('--last_row', help='Last row to read', default=20)
    args = parser.parse_args()

    tags = create(args.source, args.first_row, args.last_row)
    dump(args.destination, tags)
