#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" check.py Checks filename for proper order and keys of descriptors """

import os
import glob
import shutil

from argparse import ArgumentParser


def check(header, src, dst):
    """
    Checks each filename for codenames of header in sequence

    Args:
        path (str): path to data files
    """
    with open(header) as f:
        content = f.read().splitlines()

    HEADER = [set(line.split()[2:]) for line in content]

    for pathname in glob.iglob(src + "*.csv", recursive=True):
        (dirname, filename) = os.path.split(pathname)
        (name, extension) = os.path.splitext(filename)

        title = name.strip().split("_")
        title = fix(title)

        is_match = list()
        p = list()
        for i, item in enumerate(HEADER):
            try:
                is_match.append(title[i] in item)
                p.append((title[i], title[i] in item))
            except IndexError:
                pass

        if dst is not None and all(is_match):
            #new_dst = dst + os.path.basename(os.path.dirname(pathname)
            os.makedirs(dst, exist_ok=True)
            new_file = dst + '_'.join(map(str, title)) + extension
            shutil.copy(pathname, new_file)
            #print('\u2714 {}'.format(title))

        else:
            print('\u2718 {}'.format(title))
            print(is_match)


def fix(title):
    """
    Fixes particular known issues in filename

    0 6  t r a j e c t o r y - t i m e - d e f i n i t i o n - p o i n t 
    07 fixed-route
    08 calculation-method

    """
    trajectory_time_definition_point_corrections = {
        '1': '01-frt-1001',
        '2': '02-frt-1002',
        '3': '03-frt-1003',
        '4': '04-frt-1004',
        '5': '05-frt-1005',
        '6': '06-frt-1006',
        '7': '07-frt-1007',
        '8': '08-frt-1008'}

    fixed_route_corrections = {
        '1': '01-frt-1001',
        '2': '02-frt-1002',
        '3': '03-frt-1003',
        '4': '04-frt-1004',
        '5': '05-frt-1005',
        '6': '06-frt-1006',
        '7': '07-frt-1007',
        '8': '08-frt-1008'}

    calculation_method_corrections = {
        'sng': '01-sng',
        'uni': '02-uni',
        'rep': '03-rep'}

    fixed_route = title[6]
    calculation_method = title[7]

    title[6] = fixed_route_corrections.get(fixed_route[-1:])
    title[7] = calculation_method_corrections.get(calculation_method[-3:])

    return title


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help='Path to header file', required=True)
    parser.add_argument('-s', '--source', help='Path to source files', required=True)
    parser.add_argument('-d', '--destination', help='Path to destination files', required=False)
    args = parser.parse_args()

    check(args.file, args.source, args.destination)
