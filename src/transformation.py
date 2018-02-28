#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" transformation.py """


def get_header(src):
    """
    Creates a lists of columns from a file

    Args:
        src (str): path of source
    """
    with open(src, mode='r') as f:
        content = f.readline()
        return content.strip().split(sep=';')


def get_replacement(src, index_key, index_value):
    """
    Creates a dictionary of substitutions

    Args:
        src (str): path of source
        index_key (int):
        index_value (int):
    """
    with open(src, mode='r') as f:
        content = f.readlines()
        lines = [line.strip().split(',') for line in content]

        keys = [line[index_key] for line in lines]
        values = [line[index_value] for line in lines]

        return dict(zip(keys, values))
