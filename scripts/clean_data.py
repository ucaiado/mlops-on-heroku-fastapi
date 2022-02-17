#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clean raw data


@author: ucaiado

Created on 07/02/2022
"""

import pandas as pd
import argparse
import textwrap
from collections import OrderedDict


if __name__ == '__main__':
    s_txt = '''\
            Clean data passed and save to output path defined
            '''
    # include and parse variables
    obj_formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=obj_formatter, description=textwrap.dedent(s_txt))

    parser.add_argument(
        '-i',
        '--input',
        default=None,
        type=str,
        metavar='',
        required=True,
        help='Input file to remove spaces'
    )

    parser.add_argument(
        '-o',
        '--output',
        default=None,
        type=str,
        metavar='',
        required=True,
        help='Cleaned output file'
    )

    # recover arguments
    args = parser.parse_args()
    s_input = args.input
    s_output = args.output

    # ...
    df = pd.read_csv(s_input)
    d_data = OrderedDict()
    for s_col, df_data in df.iteritems():
        try:
            df_data = df_data.str.strip()
        except AttributeError:
            pass
        d_data[s_col.strip()] = df_data

    df_rtn = pd.DataFrame(d_data)
    df_rtn.to_csv(s_output, index=False)
    print('... saving file')